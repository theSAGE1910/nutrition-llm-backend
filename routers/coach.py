import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import google.generativeai as genai

from database import NutritionLog, get_db

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

router = APIRouter(
    prefix="/coach",
    tags=["AI Coach"]
)

@router.get("/assessment/")
def get_ai_assessment(target_protein: int = 150, db: Session = Depends(get_db)):
    all_meals = db.query(NutritionLog).all()
    
    if not all_meals:
        return {"message": "You haven't logged any meals yet! Go eat!"}
        
    total_protein = sum([meal.protein_grams for meal in all_meals])
    total_calories = sum([meal.calories for meal in all_meals])

    system_prompt = f"""
    You are a strict but motivating bodybuilding coach specializing in hypertrophy.
    Your client has eaten {total_calories} calories and {total_protein}g of protein today.
    Their daily protein target is {target_protein}g.
    
    Write a short, punchy 3-sentence assessment of their daily nutrition. 
    If they are under their protein target, tell them exactly what kind of meal they need to eat next.
    Do not use pleasantries. Get straight to the point.
    """
    
    print("Calling the AI... this might take a second.")
    response = model.generate_content(system_prompt)
    
    return {
        "daily_stats": {
            "protein": total_protein,
            "calories": total_calories,
            "target": target_protein
        },
        "coach_feedback": response.text
    }