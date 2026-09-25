from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

import models

sqlite_file_name = "dev.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]
# Request is going to hit a route handler
# A route handler with have a dependency on get_session
# get_session will create a database session
# get_session will yield/seed control to the route handler
# route handler will finish up
# the context manager (with) will clean up the session
