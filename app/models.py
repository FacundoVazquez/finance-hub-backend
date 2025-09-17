from sqlalchemy import Column, Integer, String

from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    price = 0.0
    change_pct = 0.0
    volume = 0
    indicators = {}
