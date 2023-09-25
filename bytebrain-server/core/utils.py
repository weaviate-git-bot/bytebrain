from typing import Dict, List, TypeVar

import hashlib

T = TypeVar('T')


def calculate_md5_checksum(text):
    data = text.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    md5_checksum = md5_hash.hexdigest()
    return md5_checksum


def identify_removed_snippets(
        old: Dict[str, List[str]],
        new: Dict[str, List[str]]
) -> List[str]:
    removed_files: List[str] = []
    for key, values in old.items():
        if key not in new:
            removed_files.append(key)
    return removed_files


def identify_changed_files(
        original: Dict[str, List[str]],
        new: Dict[str, List[str]]) -> List[str]:
    changed_files: List[str] = []
    for file_path, hashes in new.items():
        if file_path not in original:
            changed_files.append(file_path)
        else:
            original_hashes = original[file_path]
            if len(hashes) != len(original_hashes):
                changed_files.append(file_path)
            elif set(hashes) != set(original_hashes):
                changed_files.append(file_path)
    return changed_files


def create_dict_from_keys_and_values(keys: List[str], values: List[T]) -> Dict[str, List[T]]:
    assert (len(keys) == len(values))

    id_doc_dict = {}

    if len(keys) == 0:
        return id_doc_dict

    for i, file_path in enumerate(keys):
        if file_path in id_doc_dict:
            id_doc_dict[file_path].append(values[i])
        else:
            id_doc_dict[file_path] = [values[i]]
    return id_doc_dict


def split_string_preserve_suprimum_number_of_lines(input_string: str, chunk_size: int) -> List[str]:
    """
    Split an input string into smaller chunks while preserving as many lines as possible in each chunk.

    This function takes an input string and a chunk size as arguments and splits the string into smaller chunks
    such that the number of lines in each chunk is maximized while ensuring that the total characters in each
    chunk do not exceed the specified chunk size.
    """

    def loop(lines: List[str], chunks: List[str], chunk_size: int):
        if len(lines) == 0:
            return chunks

        current_line = lines[0]

        if len(lines[1:]) == 0:
            if len(current_line) < chunk_size:
                chunks.append(current_line)
                return loop(lines=[], chunks=chunks, chunk_size=chunk_size)
            else:
                new_chunk = current_line[0:chunk_size]
                remaining_chunked_line = current_line[chunk_size:]
                chunks.append(new_chunk)
                return loop([remaining_chunked_line] if len(remaining_chunked_line) != 0 else [], chunks,
                            chunk_size)
        for i in range(len(lines[1:])):
            next_line = lines[i + 1]
            remaining_lines = lines[i + 1:]
            if len(current_line) > chunk_size:
                new_chunks = current_line[0:chunk_size]
                remaining_chunked_line = current_line[chunk_size:]
                chunks.append(new_chunks)
                return loop([remaining_chunked_line] + remaining_lines, chunks, chunk_size)
            if len(current_line) + len(next_line) + 1 <= chunk_size:
                new_chunk = current_line + '\n' + next_line
                return loop([new_chunk] + lines[2:], chunks, chunk_size)
            if len(current_line) + len(next_line) + 1 > chunk_size:
                new_chunk = current_line
                chunks.append(new_chunk)
                return loop(remaining_lines, chunks, chunk_size)
            else:
                return chunks

        return chunks

    return loop(input_string.splitlines(), [], chunk_size)