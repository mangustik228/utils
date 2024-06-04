from typing import Literal

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    surname: str | None = None


class RoleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Literal["admin", "guest", "moderator"]

