from sqlalchemy import Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from river_flows.orm.base import Base
from river_flows.orm.mixins import TimestampMixin


class ONI(Base, TimestampMixin):
    __tablename__ = "oni"

    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    djf: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    jfm: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    fma: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    mam: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    amj: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    mjj: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    jja: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    jas: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    aso: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    son: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    ond: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    ndj: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
