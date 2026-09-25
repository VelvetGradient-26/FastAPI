from contextlib import asynccontextmanager
from typing import Annotated, Literal

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Query,
    Response,
    status,
)
from fastapi.staticfiles import StaticFiles
from sqlmodel import select

from database import SessionDependency, create_db_and_tables
from models import AppCookies, AppHeaders, RoomQueryParams

openapi_tags = [
    {"name": "rooms", "description": "all the endpoints under the rooms category"}
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    # Additional operations before the server starts up
    yield
    # Additional operations after the server shuts up


# App Description (Viewable in the swagger docs)
app = FastAPI(
    lifespan=lifespan,
    title="Rent-A-Room",
    description="Book a stay in a house or room",
    version="1.0.0",
    contact={"name": "Deepak", "email": "deepakkrishna2206@gmail.com"},
)

# present static files
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

FAQ = {
    "When is the checkin?": "6AM",
    "When is the checkout?": "24 hours after you checkin",
}

ROOMS = [
    {
        "id": 1,
        "name": "3BHK",
        "price_per_night": 200,
        "bedrooms": 3,
        "bathrooms": 2,
    },
    {
        "id": 2,
        "name": "Nisarga Nilaya",
        "price_per_night": 2000,
        "bedrooms": 5,
        "bathrooms": 3,
    },
    {
        "id": 3,
        "name": "Deluxe Suite",
        "price_per_night": 1500,
        "bedrooms": 2,
        "bathrooms": 1,
    },
]


# Home Page
@app.get("/", status_code=200, summary="Home Page!!")
def home(
    app_cookies: Annotated[AppCookies, Cookie()],
    app_headers: Annotated[AppHeaders, Header()],
    session: SessionDependency,
):
    db_result = session.exec(select(5)).one()

    greetings = {
        "en": "Welcome to Rent a Room",
        "es": "Bienvenido a Rent a Room",
        "fr": "Bienvenue a Rent a Room",
    }

    greeting = greetings.get(app_cookies.language or "en")

    return {
        "message": greeting,
        "user_agent": app_headers.user_agent,
        "db_result": db_result,
    }


@app.get("/rooms")
def display_all_rooms():
    return ROOMS


@app.get("/rooms/search", tags=["rooms"])
def get_rooms(params: Annotated[RoomQueryParams, Query()]):
    result = []
    for room in ROOMS:
        if params.search.lower() in room["name"].lower():
            if params.max_price is None or room["price_per_night"] <= params.max_price:
                result.append(room)
    return result


@app.get("/rooms/faq", tags=["rooms"])
def frequently_asked_questions():
    return FAQ


@app.get("/rooms/{id}", tags=["rooms"])
def get_room_by_id(id: int) -> dict:
    for room in ROOMS:
        if room["id"] == id:
            return room
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# Set Cookies!!
@app.get("/preferences", status_code=status.HTTP_200_OK, tags=["Cookies/preferences"])
def set_preferences(response: Response):
    app_cookies = AppCookies()

    response.set_cookie(key="theme", value=app_cookies.theme)
    response.set_cookie(key="language", value=app_cookies.language)
    return {"message": "Preferences updated!!"}


def get_number():
    return 42


@app.get("/example")
def fake_route(number: Annotated[int, Depends(get_number)]):
    return {"message": number}
