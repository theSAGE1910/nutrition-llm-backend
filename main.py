from fastapi import FastAPI, Depends
from database import engine, Base
from routers import meals, coach

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(meals.router)
app.include_router(coach.router)