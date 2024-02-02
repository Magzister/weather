from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import MultipleResultsFound

from app.db.db_config import engine
from app.db.models import Base, SeaSurfaceTemperature
from app.exceptions import NoResultError
from app.exceptions import MultipleResultsError
from app.web_pserser.parser import SST
from app.types import Hyperlink


class DB:
    def __init__(self) -> None:
       Base.metadata.create_all(engine)

    def get_sst_hyperlink(self, country: str, city: str) -> Hyperlink:
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

    def populate_sst_table(self, sst_list: list[SST]) -> None:
        stmt = delete(SeaSurfaceTemperature)
        sst_models_list = [SeaSurfaceTemperature(country=sst.country,
                                                 city=sst.city,
                                                 hyperlink=sst.href)
                           for sst in sst_list]
        with Session(engine) as session:
            session.execute(stmt)
            session.add_all(sst_models_list)
            session.commit()
