from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints, field_validator
from sqlmodel import Field, SQLModel


class Room(SQLModel, table=True):
    __tablename__: str = "rooms"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    price_per_night: int = Field()
    bedrooms: float = Field(multiple_of=0.5)
    bathrooms: float = Field(multiple_of=0.5)


class AppCookies(BaseModel):
    theme: Literal["light", "dark"] = "light"
    language: Literal["en", "es", "fr"] = "en"


class AppHeaders(BaseModel):
    user_agent: str | None


class RoomQueryParams(BaseModel):
    max_price: int | None = Field(default=None, ge=10, le=10_000)
    search: Annotated[str | None, StringConstraints(to_lower=True)] = Field(
        default=None,
        min_length=3,
        max_length=10,
        title="Search Term",
        description="Provide a keyword to look for within the room's title",
    )

    @field_validator("search")
    @classmethod
    def fail_if_funny(cls, search: str) -> str:
        if "lol" in search:
            raise ValueError("WHAT'S FUNNY IN THIS?")
        return search
