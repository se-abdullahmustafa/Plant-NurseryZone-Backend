from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib

Base = declarative_base()

class DBHandler:
    server = 'ABDULLAH'
    database = 'Nursery Plant Zone'
    username = 'sa'
    password = '12345'
    params = urllib.parse.quote_plus(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
)

    def __init__(self):
        connection_string = f'mssql+pyodbc:///?odbc_connect={self.params}'
        self.engine = create_engine(connection_string, echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.session=self.SessionLocal()
    def close(self):
        self.session.close()
def get_db():
    db = DBHandler()
    try:
        yield db.session
    finally:
        db.close()
        