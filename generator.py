import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from schema import StudySummary

# Load environment variables from the .env file
load_dotenv()

# Initialize the Gemini client
client = genai.Client()

def generate_study_materials(text_input: str) -> StudySummary:
    prompt = f"Analyze the following study material, summarize key concepts, and create active-recall flashcards:\n\n{text_input}"
    
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StudySummary,
            temperature=0.2,
        ),
    )
    
    return response.parsed