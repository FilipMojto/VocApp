import uvicorn
import argparse

from .dbconfig import Base, get_engine, get_session_local, init_db, get_database_url
from .seeding.seeding import seed_data
from .crud.models import *
from .models import *
from .dbschemas import truncate_schema


def parse_args():
    parser = argparse.ArgumentParser(description="Launch FastAPI with custom DB config")
    parser.add_argument("--db-type", choices=["sqlite", "postgresql"], default="sqlite")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default="5432")
    parser.add_argument("--user", default="postgres")
    parser.add_argument("--password", default="postgres")
    parser.add_argument("--dbname", default="./backend/data/vocapp.db")
    parser.add_argument("--api-host", default="127.0.0.1")
    parser.add_argument("--api-port", default=8000, type=int)
    parser.add_argument("--truncate-db", action="store_true", required=False)
    parser.add_argument("--seed", default=None, type=str, required=False)
    return parser.parse_args()


args = parse_args()

db_url = get_database_url(
    db_type=args.db_type,
    user=args.user,
    password=args.password,
    host=args.host,
    port=args.port,
    dbname=args.dbname,
)

engine = get_engine(db_url)
SessionLocal = get_session_local(engine)
init_db(db_url)
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    if args.truncate_db:
        truncate_session = SessionLocal()
        connection = truncate_session.connection()
        raw_conn = connection.connection
        # cursor = raw_conn.cursor()
        raw_conn.executescript(truncate_schema)
        print("Truncation complete")
        raw_conn.close()
        connection.close()
        # truncate_session.commit()
        truncate_session.close()
    if args.seed:
        seeding_session = SessionLocal()
        
        seed_data(seeder=args.seed, db=seeding_session)
        seeding_session.close()
        
    uvicorn.run("backend.api.api:app", host=args.api_host, port=args.api_port, reload=True)
