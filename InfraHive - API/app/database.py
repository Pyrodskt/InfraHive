from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib.parse, pyodbc, os
from dotenv import load_dotenv

load_dotenv()
driver= os.getenv("SQL_DRIVER")
server = os.getenv("HOSTING_SERVER")
database = os.getenv("HOSTING_DB")
username = os.getenv("HOSTING_DB_USER")
password = os.getenv("HOSTING_DB_USER_PWD")

params = urllib.parse.quote_plus(
    f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
)
connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(connection_string)

# `SessionLocal` esst une fabrique de sessions, elle ne crée pas de session elle-même.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()