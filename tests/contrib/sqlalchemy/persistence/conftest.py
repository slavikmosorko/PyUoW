from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

TEST_DB_SCHEMA = Path(__file__).parent / "test_db_schema.sql"


@pytest.fixture(scope="package", autouse=True)
async def migrated_db(engine: AsyncEngine) -> None:
    async with engine.connect() as conn, conn.begin():
        sql_instructions = TEST_DB_SCHEMA.read_text(encoding="utf-8")
        statements = sql_instructions.split(";")
        for statement in statements:
            await conn.execute(text(statement))
