from sqlalchemy import text
from app.database import Base
import app.models
from sqlalchemy import inspect

def test_database_connection(test_engine) :
    with test_engine.connect() as connection :
        database_name = connection.execute(text("SELECT current_database()")).scalar_one()

    assert database_name == "personal_note_library_test"

def test_table_exist(test_engine) :
    table_names = inspect(test_engine).get_table_names()

    assert "users" in table_names
    assert "notes" in table_names
    assert "refreshtokens" in table_names