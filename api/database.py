"""Database connection pool for the FastAPI app."""
import os
from psycopg_pool import ConnectionPool
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://efinmap_user:yourpassword@localhost:5432/efinmap")

_pool: ConnectionPool | None = None


def init_pool():
    global _pool
    _pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=10, open=True)


def close_pool():
    if _pool:
        _pool.close()


@contextmanager
def get_db():
    if _pool is None:
        init_pool()
    with _pool.connection() as conn:
        yield conn
