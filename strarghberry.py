"""
Run with

    uvicorn strarghberry:app --port 8888 --reload



$ ab -c 5 -n 10 "localhost:8888/graphql?query=%7Bsync%7D" | grep "Time taken"
Time taken for tests:   10.043 seconds

$ ab -c 5 -n 10 "localhost:8888/graphql?query=%7BaSync%7D" | grep "Time taken"
Time taken for tests:   3.031 seconds

$ ab -c 5 -n 10 "localhost:8888/graphql?query=%7BsyncInExecutor%7D" | grep "Time taken"
Time taken for tests:   3.040 seconds

ab -c 5 -n 10 "localhost:8888/graphql?query=%7BsyncWithDecorator%7D" | grep "Time taken"
Time taken for tests:   3.034 seconds
"""

import time
import asyncio
from fastapi import FastAPI

import strawberry
from strawberry.fastapi import GraphQLRouter
from decorator import force_run_in_executor, check_schema

app = FastAPI()


def sync_long_running():
    time.sleep(1)


async def async_long_running():
    await asyncio.sleep(1)


@strawberry.type
class Query:
    @strawberry.field
    def sync(self) -> str:
        sync_long_running()
        return "Hello World"

    @strawberry.field
    async def a_sync(self) -> str:
        await async_long_running()
        return "Hello World"

    @strawberry.field
    async def sync_in_executor(self) -> str:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, sync_long_running)
        return "Hello World"

    @strawberry.field
    @force_run_in_executor
    def sync_with_decorator(self) -> str:
        sync_long_running()
        return "Hello World"


@strawberry.type
class Mutation:
    @strawberry.mutation
    def do_something(self, arg: str) -> bool:
        return False

    @strawberry.mutation
    @force_run_in_executor
    def do_something_else(self, arg: str) -> bool:
        return False


schema = strawberry.Schema(Query, mutation=Mutation)

check_schema(schema, strict=False)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
