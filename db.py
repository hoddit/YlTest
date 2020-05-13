from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite?check_same_thread=False', echo=False)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    subject_name_index = Column(Integer)
    theme = Column(String)


class SubjectName(Base):
    __tablename__ = 'subject_names'

    id = Column(Integer, primary_key=True)
    rus_name = Column(String)


class TestPassInfo(Base):
    __tablename__ = 'tests_pass_info'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    test_id = Column(Integer)
    result = Column(Integer)


Session = sessionmaker(bind=engine)
