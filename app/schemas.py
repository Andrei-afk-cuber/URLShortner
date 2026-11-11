from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


# Link validate schema
class LinkBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    original_url: HttpUrl


# Public link scheme
class LinkPublic(LinkBase):
    code: str
    created_at: datetime
    clicks: int


# Redis link scheme
class LinkRedis(LinkPublic):
    id: int
