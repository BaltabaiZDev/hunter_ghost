# db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base,GameResult
from datetime import datetime

engine = create_engine('sqlite:///game.db')  # немесе postgres/mysql
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def save_result(nickname, hp, score, level, start_time, end_time):
    session = Session()
    result = GameResult(
        nickname=nickname,
        hp=hp,
        score=score,
        level=level,
        start_time=start_time,
        end_time=end_time
    )
    session.add(result)
    session.commit()
    session.close()
