from typing import Optional

from fastapi import WebSocket
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.chat_vector_db.prompts import (CONDENSE_QUESTION_PROMPT)
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

from core.llm.callbacks import StreamingLLMCallbackHandler
from core.custom_conversational_chain import ConversationalRetrievalChainWithCustomPrompt
from core.upgrade_sqlite import upgrade_sqlite_version


def make_doc_search(persistent_dir: str):
    upgrade_sqlite_version()
    return Chroma(
        persist_directory=persistent_dir,
        embedding_function=OpenAIEmbeddings()
    )


question_generator = LLMChain(
    llm=ChatOpenAI(
        client=OpenAI,
        streaming=False,
        callbacks=[StreamingStdOutCallbackHandler()],
        temperature=0,
        verbose=False
    ),
    prompt=CONDENSE_QUESTION_PROMPT,
    verbose=False
)


def make_combine_docs_chain(websocket: Optional[WebSocket]):
    return load_qa_chain(
        ChatOpenAI(
            client=OpenAI,
            streaming=True,
            callbacks=[(StreamingLLMCallbackHandler(websocket))] if websocket is not None else [],
            temperature=0,
            verbose=False
        ),
        chain_type="stuff",
        verbose=False
    )


def make_question_answering_chatbot(websocket: Optional[WebSocket], persistent_dir: str, prompt_template: str):
    return ConversationalRetrievalChainWithCustomPrompt(
        combine_docs_chain=make_combine_docs_chain(websocket),
        retriever=make_doc_search(persistent_dir).as_retriever(),
        question_generator=question_generator,
        get_chat_history=get_chat_history,
        return_source_documents=True,
        prompt_refactor_template=lambda query: generate_prompt(prompt_template, query),
        max_tokens_limit=3700
    )


def generate_prompt(prompt_template: str, query: str) -> str:
    return prompt_template.replace("{query}", query)


def get_chat_history(chat_history) -> str:
    return "\n\n".join(chat_history)
