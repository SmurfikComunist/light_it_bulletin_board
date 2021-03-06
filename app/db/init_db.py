from app.db import base  # noqa
from app.db.session import engine

# make sure all SQL Alchemy models are
# imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details:
# https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db() -> None:
    base.Base.metadata.create_all(bind=engine)
