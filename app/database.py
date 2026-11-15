import os
import socket
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Environment-based configuration with production-grade defaults
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/hotel_booking",
)

# Ensure psycopg2 driver is explicitly used when generic postgresql:// is provided
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# If DATABASE_URL points to docker container hostname 'db' but host cannot resolve it (e.g. local host runs),
# seamlessly fallback to localhost
if "@db:5432" in DATABASE_URL:
    try:
        socket.gethostbyname("db")
    except socket.gaierror:
        DATABASE_URL = DATABASE_URL.replace("@db:5432", "@localhost:5432")

# Connect args & engine tuning for high concurrency
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initializes PostgreSQL extensions, tables, and exclusion constraints.
    Enables btree_gist extension required for EXCLUDE USING gist constraints.
    """
    is_postgres = engine.dialect.name == "postgresql"

    if is_postgres:
        with engine.connect() as conn:
            # Enable btree_gist extension automatically on startup
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gist;"))
            conn.commit()

    # Create all tables defined in metadata
    Base.metadata.create_all(bind=engine)

    if is_postgres:
        with engine.connect() as conn:
            # Verify and ensure the GiST exclusion constraint exists on reservations
            conn.execute(
                text(
                    """
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM pg_constraint
                            WHERE conname = 'exclude_overlapping_confirmed_reservations'
                        ) THEN
                            ALTER TABLE reservations
                            ADD CONSTRAINT exclude_overlapping_confirmed_reservations
                            EXCLUDE USING gist (
                                room_id WITH =,
                                daterange(check_in, check_out, '[)') WITH &&
                            ) WHERE (status = 'CONFIRMED');
                        END IF;
                    END $$;
                    """
                )
            )
            conn.commit()
