import argparse
import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routers.users import router

app = FastAPI(title="FastAPI + SQLAlchemy + Alembic example")
app.include_router(router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run("main:app", host=args.host, port=args.port)
