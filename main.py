import json
from typing import Optional
from fastapi import FastAPI, Depends, Path, Body
from pydantic import BaseModel

from Helper.load_data import load_markdown
from Helper.split import split_documents
from embeding import create_embeding
from faiss_indexer import FaissIndexer
from Helper.query import generate_answer_from_context
from Helper.Database import *
from schemas import CreateUserIn, MessageIn
from fastapi.middleware.cors import CORSMiddleware

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app = FastAPI()

# Paths
DATA_DIR = "data"
FAISS_INDEX_PATH = f"{DATA_DIR}/faiss_index.idx"
METADATA_PATH = f"{DATA_DIR}/data.json"

# Load env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
origins = ['http://localhost:5173']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # lub ["*"] żeby pozwolić wszystkim (uwaga: niezalecane na produkcji)
    allow_credentials=True,
    allow_methods=["*"],              # można zawęzić do np. ["GET", "POST"]
    allow_headers=["*"],              # lub konkretnie np. ["Authorization", "Content-Type"]
)

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# --- ENDPOINTY ---
def get_markdown_files_recursive(base_path: str) -> list[str]:
    markdown_files = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                markdown_files.append(full_path)
    return markdown_files


@app.get("/")
def home():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r') as file:
            files = json.load(file)
        return files
    return {"message": "Brak danych."}


@app.get("/create")
def create_database():
    files = get_markdown_files_recursive(
        "/Users/wojciechmankowski/Library/CloudStorage/OneDrive-Osobisty/Baza wiedzy 2")

    documents = []
    for file in files:
        documents.extend(load_markdown(file))
    chunks = split_documents(documents)

    texts = [chunk.page_content for chunk in chunks]
    embeddings = create_embeding(texts)

    indexer = FaissIndexer(dimension=embeddings.shape[1])
    indexer.add_vectors(embeddings)
    indexer.save_index(FAISS_INDEX_PATH)

    metadata = [
        {
            "id": i,
            "text": chunk.page_content,
            "source": chunk.metadata.get("source", "unknown")
        }
        for i, chunk in enumerate(chunks)
    ]
    with open(METADATA_PATH, "w", encoding="utf-8", errors="replace") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return {"status": "success", "chunks": len(chunks)}

class Ask(BaseModel):
    question: str
    session: int

@app.post("/ask/")
def get_ask(question: Ask = Body(...), supabase: Client = Depends(get_supabase)):
    if not os.path.exists(FAISS_INDEX_PATH):
        return {"error": "Baza danych nie została jeszcze utworzona. Najpierw wywołaj /create"}
    messages = get_messages_for_session(question.session, supabase)
    add_message(question.session, 'user',question.question, supabase)
    indexer = FaissIndexer(dimension=768, index_path=FAISS_INDEX_PATH)
    query_embedding = indexer.create_embedding([question.question, messages])
    distances, indices = indexer.search(query_embedding, k=2)

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    top_chunks = [metadata[i] for i in indices[0] if i < len(metadata)]
    context = "\n".join([chunk["text"] for chunk in top_chunks])
    answer = generate_answer_from_context(f'Pytanie: {question.question}, odpowiedzi w ramach tej samej sesji: {messages}', context)
    add_message(question.session, 'ai', answer["answer"], supabase, {"sources": list(set(chunk["source"] for chunk in top_chunks))})

    return {
        "question": question,
        'answer': answer['answer'],
        "sources": list(set(chunk["source"] for chunk in top_chunks))
    }


@app.post("/user")
def create_user_endpoint(user: CreateUserIn, supabase: Client = Depends(get_supabase)):
    data = create_user(user.username, user.email, supabase)
    return {"data": data}


@app.post("/session/{user_id}")
def create_session(user_id: int, title: Optional[str] = None, supabase: Client = Depends(get_supabase)):
    session = create_chat_session(user_id, supabase, title)
    return {"data": session}


@app.post("/message/")
def post_message(message: MessageIn, supabase: Client = Depends(get_supabase)):
    data = add_message(
        session_id=message.session_id,
        sender_type=message.sender_type,
        content=message.content,
        supabase=supabase,
        metadata=message.metadata
    )
    return {"data": data}


@app.get("/sessions/{user_id}")
def get_user_sessions(user_id: int = Path(...), supabase: Client = Depends(get_supabase)):
    response = get_sessions_for_user(user_id, supabase)
    return {"data": response}

@app.post("/new/sessions/{user_id}")
def new_sessions(user_id: int = Path(...), supabase: Client = Depends(get_supabase)):
    response = add_session(user_id, supabase)
    return {"data": response}

@app.get("/messages/{session_id}")
def get_session_messages(session_id: int = Path(...), supabase: Client = Depends(get_supabase)):
    response = get_messages_for_session(session_id, supabase)
    return {"data": response}

@app.get("/ping")
async def ping():
    return {"msg": "pong"}

# uvicorn main:app --reload
# ollama run gemma3:4b
