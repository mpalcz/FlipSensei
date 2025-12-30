# ranking metadata, ml confidence, explainability fields
from pydantic import BaseModel
from typing import List

class Recommendation(BaseModel):
    id: int
    score: float

class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation]
