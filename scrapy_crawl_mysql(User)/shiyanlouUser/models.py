from sqlalchemy import Date
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqldb://root@localhost:3306/shiyanlou?charset=utf8')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    type = Column(String(64))
    status = Column(String(64), index=True)
    school = Column(String(64))
    job = Column(String(64))
    level = Column(Integer, index=True)
    join_date = Column(Date)
    learn_courses_num = Column(Integer)

if __name__=='__main__':
    Base.metadata.create_all(engine)
