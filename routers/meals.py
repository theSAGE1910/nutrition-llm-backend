from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import NutritionLog, MealCreate, get_db

router = APIRouter(
    prefix="/meals",
    tags=["Meals"]
)

@router.post("/log-meal/")
def log_meal(meal: MealCreate, db: Session = Depends(get_db)):
    db_meal = NutritionLog(
        meal_name=meal.meal_name, 
        protein_grams=meal.protein_grams, 
        calories=meal.calories)
    
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)

    return {"message": "Meal logged successfully!", "data": db_meal}

@router.get("/daily-summary/")
def get_summary(db: Session = Depends(get_db)):
    all_meals = db.query(NutritionLog).all()

    total_protein = sum([meal.protein_grams for meal in all_meals])
    total_calories = sum([meal.calories for meal in all_meals])

    return {"total_protein": total_protein, 
            "total_calories": total_calories, 
            "meals": all_meals}