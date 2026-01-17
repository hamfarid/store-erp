import os
import time
import threading
import sqlite3
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool


def make_engine(db_path: str):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    engine = create_engine(
        f"sqlite:///{db_path}",
        poolclass=NullPool,
        connect_args={
            "check_same_thread": False,
            "timeout": 30,
        },
        echo=False,
    )

    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):  # noqa: ARG001
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA busy_timeout=5000")
            finally:
                cursor.close()

    return engine


def attempt_write_lock(engine, result: dict):
    # Try to acquire a write lock while another connection holds it.
    conn = engine.raw_connection()
    try:
        cur = conn.cursor()
        t0 = time.time()
        cur.execute("BEGIN IMMEDIATE")  # should block until lock released
        elapsed = time.time() - t0
        # Immediately commit to release
        conn.commit()
        result["ok"] = True
        result["elapsed"] = elapsed
    except Exception as e:  # pragma: no cover
        result["ok"] = False
        result["error"] = str(e)
    finally:
        try:
            conn.close()
        except Exception:
            pass


def main():
    base_dir = os.path.join(os.getcwd(), "instance")
    db_path = os.path.join(base_dir, "locktest_smoke.db")

    # Ensure clean slate
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass

    engine = make_engine(db_path)

    # Connection A acquires a write lock
    conn1 = engine.raw_connection()
    cur1 = conn1.cursor()
    cur1.execute("BEGIN IMMEDIATE")  # acquire write lock

    # Start thread that attempts to acquire write lock (should block until release)
    result = {}
    t = threading.Thread(target=attempt_write_lock, args=(engine, result))
    t.start()

    # Hold the lock briefly, then release
    time.sleep(1.0)
    conn1.commit()
    conn1.close()

    t.join(timeout=10)

    if not result.get("ok"):
        print(f"FAIL: second writer error: {result.get('error')}")
        raise SystemExit(1)

    elapsed = result.get("elapsed", 0.0)
    # We expect the second writer to have blocked for ~1s (>=0.9s here)
    if elapsed >= 0.9:
        print(
            f"OK: busy_timeout respected; second writer waited {elapsed:.2f}s and succeeded"
        )
        raise SystemExit(0)

    print(f"WARN: second writer wait too short: {elapsed:.2f}s (still succeeded)")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
