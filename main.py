from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict,Any
from fastapi.middleware.cors import CORSMiddleware

from encoder import ProductEncoder
from recommender import Recommender

app = FastAPI()

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize once at startup
encoder = ProductEncoder("products.json")
recommender = Recommender(encoder, n_neighbors=3)

class FilterRequest(BaseModel):
    category: str
    filters: Dict[str, Any]

@app.post("/recommend")
def recommend_products(request: FilterRequest):
    results = recommender.recommend(request.filters)
    return {"recommendations": results}
@app.get("/")
def root():
    return {"message": "Website is live"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)