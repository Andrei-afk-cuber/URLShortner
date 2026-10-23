from datetime import datetime

from pydantic import BaseModel, HttpUrl


# Link validate schema
class LinkBase(BaseModel):
    original_url: HttpUrl


# Public link scheme
class LinkPublic(LinkBase):
    code: str
    created_at: datetime
    clicks: int