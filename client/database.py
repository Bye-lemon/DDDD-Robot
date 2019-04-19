import sys
from datetime import datetime

from sqlalchemy import INTEGER, TIMESTAMP, VARCHAR, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import config

reload(sys)
sys.setdefaultencoding('utf-8')

Base = declarative_base()


class Message(Base):
    __tablename__ = "Message"

    message = Column(VARCHAR(1024))
    timestamp = Column(TIMESTAMP, primary_key=True)
    TTL = Column(INTEGER, default=10)

    def __init__(self, message, timestamp):
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return "<Message %s>" % self.message


class DB():
    def __init__(self):
        db_config = config.get('database')
        engine = create_engine("mysql+mysqldb://{user}:{password}@{host}:{port}/{database}?charset=utf8".format(
            user=db_config['user'], password=db_config['password'], host=db_config[
                'host'], port=db_config['port'], database=db_config['database']
        ), encoding="utf-8")
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def send_message(self, message):
        now = datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        test = Message(message=message, timestamp=time)
        self.session.rollback()
        self.session.add(test)
        self.session.commit()
        self.session.close()
