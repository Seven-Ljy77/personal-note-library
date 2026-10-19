import pytest
from app.main import app
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from sqlalchemy import text
from app.database import Base


@pytest.fixture
def client(test_engine):

    TestSessionLocal = sessionmaker(
        bind = test_engine
    )

    def get_test_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db

    try:
        with TestClient(app) as c:
            yield c
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def test_engine():
    load_dotenv()
    TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]

    assert make_url(TEST_DATABASE_URL).database == "personal_note_library_test"

    test_engine = create_engine(TEST_DATABASE_URL)

    # 每进行一个测试前都需要删除所有表然后建表
    try:
        with test_engine.connect() as connection :
            database_name = connection.execute(
                text("select current_database()")
            ).scalar_one()

        if database_name != "personal_note_library_test":
            raise RuntimeError("当前连接数据库不是测试数据库！")

        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)

        try :
            yield test_engine
        finally :
            Base.metadata.drop_all(bind=test_engine)
    finally:
        test_engine.dispose()