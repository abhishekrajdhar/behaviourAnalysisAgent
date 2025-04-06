# Import required libraries
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import google.api_core.exceptions
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os

# Configure Gemini API key securely
genai.configure(api_key=os.getenv("AIzaSyDm1y_Pjd_SGWoZ0kkyVta8tcsnPjFFCiE"))

# Initialize FastAPI app
app = FastAPI(title="Behavioral Interview AI Agent")

# Allow CORS (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class BehaviorRequest(BaseModel):
    role: str
    experience_level: str  # e.g., "fresher", "mid-level", "senior"
    target_company: str    # e.g., "Google", "Amazon"

# Response model
class BehaviorResponse(BaseModel):
    question: str
    advice: str = "This is a behavioral question generated by AI. Use the STAR method (Situation, Task, Action, Result) when answering."

# Prompt template for generating behavioral questions
BEHAVIOR_PROMPT_TEMPLATE = (
    "You are a professional behavioral interview coach preparing candidates for {target_company}. "
    "Generate a STAR-based behavioral interview question suitable for a {experience_level} candidate "
    "applying for a {role} role. The question should test soft skills, problem-solving, or leadership.\n\n"
    "Behavioral Interview Question:"
)

# API Endpoint
@app.post("/behavioral-interview", response_model=BehaviorResponse)
async def generate_behavioral_question(req: BehaviorRequest):
    prompt = BEHAVIOR_PROMPT_TEMPLATE.format(
        role=req.role.strip(),
        experience_level=req.experience_level.strip(),
        target_company=req.target_company.strip()
    )

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        question_text = response.text.strip()
    except google.api_core.exceptions.GoogleAPIError:
        question_text = "Apologies, I'm currently unable to generate a behavioral question. Please try again later."

    return BehaviorResponse(question=question_text)

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
