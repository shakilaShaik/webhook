# app/models.py

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class GitHubEvent(BaseModel):
    request_id: str
    author: str
    action: Literal["PUSH", "PULL_REQUEST", "MERGE"]
    from_branch: Optional[str] = None
    to_branch: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC"))
