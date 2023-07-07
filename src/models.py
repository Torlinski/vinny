"""One file to store models for pydantic, no linting for this file as it doesnt follow a lot conventions."""
# pylint: skip-file

from typing import List

from pydantic import BaseModel


class SessionPayload(BaseModel):
    """Model for Session payload"""

    status: str
    paragraphs: List[List[str]]
    commands: List[str]
    chatgpt: str
    index: int

    class Config:
        extra = 'forbid'
