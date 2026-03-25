from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware

from encoder import ProductEncoder
from recommender import Recommender

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://coolguide.live",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

recommenders = {}

def get_recommender(category: str):
    if category not in recommenders:
        if category == "air-purifier":
            recommenders[category] = Recommender(ProductEncoder("data/air_purifiers.json"))
        elif category == "air-conditioner":
            recommenders[category] = Recommender(ProductEncoder("data/air_conditioners.json"))
    return recommenders.get(category)

class FilterRequest(BaseModel):
    category: str
    filters: Dict[str, Any]

@app.post("/recommend")
def recommend_products(request: FilterRequest):
    recommender = get_recommender(request.category)

    if not recommender:
        raise HTTPException(status_code=400, detail="Invalid category")

    if not request.filters:
        raise HTTPException(status_code=400, detail="Filters cannot be empty")

    results = recommender.recommend(request.filters)

    return {"recommendations": results}

@app.get("/")
def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)