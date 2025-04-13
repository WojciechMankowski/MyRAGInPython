from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    all_chunks = []
    for doc in documents:
        chunks = text_splitter.split_documents([doc])
        all_chunks.extend(chunks)
    return all_chunks