import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

user = config["DB"]["user"]
password = config["DB"]["password"]
host = config["DB"]["host"]
port = config["DB"]["port"]
database = config["DB"]["database"]

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=0)
DBSession = sessionmaker(bind=engine)
session = DBSession()





