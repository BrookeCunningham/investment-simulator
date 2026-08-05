import sys
from pathlib import Path

# ensure the repo root (server) is on sys.path so `import app` works
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from app.database import engine
from sqlalchemy import text


def main():
    print("Connecting to database via SQLAlchemy engine...")
    with engine.connect() as conn:
        # ensure immediate commit for DDL
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        print("Dropping public schema (CASCADE)...")
        conn.execute(text("DROP SCHEMA public CASCADE"))
        print("Creating public schema...")
        conn.execute(text("CREATE SCHEMA public"))

    print("Schema reset complete.")


if __name__ == '__main__':
    main()
