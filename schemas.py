# schemas.py
from typing import Optional, Literal
from pydantic import BaseModel


class CreateUserIn(BaseModel):
    username: str
    email: Optional[str] = None


class MessageIn(BaseModel):
    session_id: int
    sender_type: Literal['user', 'ai', 'system']
    content: str
    metadata: Optional[dict] = None
