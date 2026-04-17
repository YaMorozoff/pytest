from fastapi import FastAPI
from database import engine, Base
from routers.users import users


def main(args=None):
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="FastAPI + SQLAlchemy + Alembic example")

    app.include_router(users.router)
    # app.include_router(products.router)
    # app.include_router(orders.router)


if __name__ == "__main__":
    main()
