from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class SeaSurfaceTemperature(Base):
    __tablename__ = "sea_surface_temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str]
    city: Mapped[str]
    hyperlink: Mapped[str]

    def __repr__(self) -> str:
        return ("SeaSurfaceTemperature("
                f"country={self.country}, "
                f"city={self.city}, "
                f"hyperlink={self.hyperlink})")
