from pydantic import BaseModel, Field
from typing import List

class Flashcard(BaseModel):
    question: str = Field(description="A concise question testing a key concept.")
    answer: str = Field(description="A clear, direct answer to the question.")

class StudySummary(BaseModel):
    key_concepts: List[str] = Field(description="Bullet points summarizing core topics.")
    flashcards: List[Flashcard] = Field(description="List of active-recall flashcards.")