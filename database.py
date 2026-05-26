from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel, Field

SQLALCHEMY_DATABASE_URL = "sqlite:///./fitness.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NutritionLog(Base):
    __tablename__ = "nutrition_logs"

    id = Column(Integer, primary_key=True, index=True)
    meal_name = Column(String, index=True)
    protein_grams = Column(Float)
    calories = Column(Integer)

class MealCreate(BaseModel):
    meal_name: str  = Field(..., min_length=2, max_length=50)
    protein_grams: float = Field(..., gt=0, lt=200)
    calories: int = Field(..., ge=0)