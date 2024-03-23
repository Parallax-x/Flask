import pydantic
from typing import Optional
from abc import ABC


class AbstractAdvert(pydantic.BaseModel, ABC):
    title: str
    description: str
    owner: str


class CreateAdvert(AbstractAdvert):
    title: str
    description: str
    owner: str


class UpdateAdvert(AbstractAdvert):
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None
