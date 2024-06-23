from unittest.mock import AsyncMock

from sqlalchemy.ext.asyncio import AsyncEngine

from pyuow.contrib.sqlalchemy.work import (
    SqlAlchemyTransaction,
    SqlAlchemyTransactionManager,
)


class TestSqlAlchemyTransaction:

    async def test_rollback_should_call_transaction_provider_original_rollback(
        self,
    ):
        # given
        trx_provider = AsyncMock()
        trx = SqlAlchemyTransaction(trx_provider)
        # when
        await trx.rollback()
        # then
        trx_provider.rollback.assert_awaited_once()

    async def test_commit_should_call_transaction_provider_original_commit(
        self,
    ):
        # given
        trx_provider = AsyncMock()
        trx = SqlAlchemyTransaction(trx_provider)
        # when
        await trx.commit()
        # then
        trx_provider.commit.assert_awaited_once()


class TestSqlAlchemyTransactionManager:
    async def test_transaction_should_return_same_session_if_called_in_already_opened_transaction(
        self, engine: AsyncEngine
    ):
        # given
        manager = SqlAlchemyTransactionManager(engine)
        # when
        async with manager.transaction() as trx:
            first_trx = trx.it().get_transaction()

            async with manager.transaction() as trx:
                second_trx = trx.it().get_transaction()
        # then
        assert first_trx == second_trx

    async def test_transaction_should_return_different_session_if_called_in_already_opened_transaction(
        self, engine: AsyncEngine
    ):
        # given
        manager = SqlAlchemyTransactionManager(engine)
        # when
        async with manager.transaction() as trx:
            first_trx = trx.it().get_transaction()

        async with manager.transaction() as trx:
            second_trx = trx.it().get_transaction()
        # then
        assert first_trx != second_trx
