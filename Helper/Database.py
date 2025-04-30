# Database.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNKCJE ---

def create_user(username, email, supabase: Client):
    response = supabase.table("users").insert({
        "username": username,
        "email": email
    }).execute()
    return response.data

def create_chat_session(user_id, supabase: Client, title=None):
    response = supabase.table("chat_sessions").insert({
        "user_id": user_id,
        "title": title
    }).execute()
    return response.data

def add_message(session_id, sender_type, content, supabase: Client, metadata=None):
    data = {
        "session_id": session_id,
        "sender": sender_type,
        "content": content,
        "metadata": metadata or {}
    }
    response = supabase.table("messages").insert(data).execute()
    return response.data

def add_session(user_id, supabase: Client):
    res = supabase.table('chat_sessions').insert({'user_id': user_id}).execute()
    return res.data

def get_messages_for_session(session_id, supabase: Client):
    response = supabase.table("messages") \
        .select("*") \
        .eq("session_id", session_id) \
        .execute()
    return response.data

def get_sessions_for_user(user_id, supabase: Client):
    response = supabase.table("chat_sessions") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("updated_at", desc=True) \
        .execute()
    return response.data

def get_user(username, supabase: Client):
    response = supabase.table("users") \
        .select("*") \
        .eq("username", username) \
        .execute()
    return response.data

# --- TEST / ENTRYPOINT ---

if __name__ == '__main__':
    # create_user("wojtek", "wojtekm510@gmail.com", supabase)
    # create_chat_session(1, supabase)
    # add_message(1, 'user', "Co to są emocje?", supabase)
    print(get_user('wojtek', supabase))
