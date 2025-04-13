import json

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document


def load_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return [Document(page_content=text, metadata={"source": file_path})]


def save_metadata(metadata, output_path="data/data.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
