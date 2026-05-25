import pytest
import asyncio
from src.task import Task
from src.executor import AsyncExecutor
from src.handlers import DefaultHandler, TaskHandler
from src.exceptions import TaskError


class FastTestHandler:
    async def handle(self, task: Task) -> None:
        task.status = "sent"


class ErrorTestHandler:
    async def handle(self, task: Task) -> None:
        raise TaskError("Специальная тестовая ошибка")


def test_handler_protocol_compliance():
    assert isinstance(DefaultHandler(), TaskHandler)
    assert isinstance(FastTestHandler(), TaskHandler)


def test_executor_processes_task():
    async def run_test():
        task = Task(task_id="test1", description="A", payload={}, priority=1, status="ready")

        async with AsyncExecutor() as executor:
            executor.register_handler("default", FastTestHandler())
            await executor.add_task(task)

        assert task.status == "sent"

    asyncio.run(run_test())


def test_executor_handles_errors_gracefully():
    async def run_test():
        task = Task(task_id="test2", description="B", payload={}, priority=1)

        try:
            async with AsyncExecutor() as executor:
                executor.register_handler("default", ErrorTestHandler())
                await executor.add_task(task)
        except Exception:
            pytest.fail("Executor не перехватил ошибку в задаче.")

    asyncio.run(run_test())