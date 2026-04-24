import argparse
import uvicorn
from fastapi import FastAPI
from routers.users import users_router
from routers.products import products_router
from routers.orders import orders_router

app = FastAPI(title="FastAPI + SQLAlchemy + Alembic example")
app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run("main:app", host=args.host, port=args.port)
