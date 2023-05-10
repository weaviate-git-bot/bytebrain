import { ChatPrompt } from './ChatPrompt';

export default {
  title: "Chat/ChatPrompt",
  component: ChatPrompt,
  tags: ["autodocs"],
  argTypes: {
    title: { name: "Title", control: { type: "text" } },
    defaultQuestion: { name: "Default Question", control: { type: "text" } },
    websocketEndpoint: { name: "Websocket Endpoint", control: { type: "text" } },
  },
};

export const ZIOChat =  {
  args: {
    title: "ZIO Chat",
    defaultQuestion: "What are the befenits of using ZIO?",
    websocketEndpoint: 'ws://localhost:8081/chat'
  }
}