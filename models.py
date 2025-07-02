#models.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class GameResult(Base):
    __tablename__ = 'game_results'
    id = Column(Integer, primary_key=True)
    nickname = Column(String, nullable=False)
    hp = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    end_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
