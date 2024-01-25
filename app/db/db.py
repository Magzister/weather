from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import MultipleResultsFound
from typing import TypeAlias

from db_config import engine
from models import Base, SeaSurfaceTemperature
from app.exceptions import NoResultError
from app.exceptions import MultipleResultsError


Hyperlink: TypeAlias = str


class DB:
    def __init__(self) -> None:
       Base.metadata.create_all(engine)

    def get_sst(self, country: str, city: str) -> Hyperlink:
        stmt = (
            select(SeaSurfaceTemperature.hyperlink)
            .where(SeaSurfaceTemperature.country == country)
            .where(SeaSurfaceTemperature.city == city)
        )
        with Session(engine) as session:
            try:
                return session.scalars(stmt).one()
            except NoResultFound:
                raise NoResultError(f"No sst for {country}, {city}.")
            except MultipleResultsFound:
                raise MultipleResultsError(f"Multiple sst for {country}, {city} in database.")
