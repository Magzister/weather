from sqlalchemy import create_engine

from app import config


engine = create_engine(config.DB_PATH)
