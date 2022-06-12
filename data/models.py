from distutils.log import fatal
from sqlalchemy import Column, String, Numeric, Integer

from data.database import Base


class Food(Base):
    __tablename__ = "foods"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String, unique=True, index=True)
    category        = Column(String, unique=True, index=True)
    kcal            = Column(Numeric(10,2))
    carbs           = Column(Numeric(10,2))
    protein         = Column(Numeric(10,2))
    fat         = Column(Numeric(10,2))
