import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware

from encoder import ProductEncoder

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

# ✅ Categories and product files
CATEGORY_FILES = {
    "air-purifier": "data/air_purifiers.json",
    "air-conditioner": "data/air_conditioners.json",
    "fridge": "data/fridges.json",
    "laptop": "data/laptops.json",
    "tv-(television)": "data/tv.json"

}

# ✅ Load recommenders (encoders) for all categories
recommenders = {}
for category, file in CATEGORY_FILES.items():
    recommenders[category] = ProductEncoder(file, category=category)

# ✅ Request schema
class FilterRequest(BaseModel):
    category: str
    filters: Dict[str, Any]

@app.post("/recommend")
def recommend_products(request: FilterRequest):
    recommender = recommenders.get(request.category)

    if not recommender:
        raise HTTPException(status_code=400, detail="Invalid category")

    if not request.filters:
        raise HTTPException(status_code=400, detail="Filters cannot be empty")

    # Encode user filters safely
    user_vector = recommender.encode_user(request.filters)
    # Compare with products (simple example: return top 5 most similar)
    from sklearn.metrics.pairwise import cosine_similarity
    similarities = cosine_similarity(user_vector, recommender.get_encoded_products())
    top_indices = similarities[0].argsort()[::-1][:5]

    results = [recommender.get_products()[i] for i in top_indices]

    return {"recommendations": results}

@app.get("/")
def root():
    return {"message": "API is running"}

# ✅ Run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)