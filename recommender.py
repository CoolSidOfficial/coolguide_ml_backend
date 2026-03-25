from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware

from encoder import ProductEncoder
from recommender import Recommender

app = FastAPI()

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://coolguide.live",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load recommenders (you can later make this lazy-loaded)
recommenders = {
    "air-purifier": Recommender(ProductEncoder("data/air_purifiers.json")),
    "air-conditioner": Recommender(ProductEncoder("data/air_conditioners.json")),
}

# ✅ Request schema
class FilterRequest(BaseModel):
    category: str
    filters: Dict[str, Any]

# ✅ Recommendation endpoint
@app.post("/recommend")
def recommend_products(request: FilterRequest):
    recommender = recommenders.get(request.category)

    if not recommender:
        raise HTTPException(status_code=400, detail="Invalid category")

    if not request.filters:
        raise HTTPException(status_code=400, detail="Filters cannot be empty")

    results = recommender.recommend(request.filters)

    return {"recommendations": results}

# ✅ Health check
@app.get("/")
def root():
    return {"message": "API is running"}

# ✅ Run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)