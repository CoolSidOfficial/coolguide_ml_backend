# Product Recommender API

## Overview

This API recommends products like **Air Purifiers, Air Conditioners, and Fridges** based on user-selected filters.  
It uses a **lightweight ML-based feature encoding and similarity matching algorithm** to rank and return the best matching products.

---

## How the ML Algorithm Works

The recommendation system uses **categorical feature encoding** and **vector similarity** to suggest products.

### 1. Product Feature Encoding

- Each product category has a JSON dataset with product details.  
- `encoder.py` converts **categorical features** (like `"Budget-Range"`, `"Machine-Brand"`) into **numeric vectors** using **OneHotEncoder**.  
- **Normalization:** Some features are standardized (e.g., `"Low cost"` → `"Budget"`) to ensure consistency.  
- **Dummy Row:** A synthetic row with all possible options is added to avoid errors if the user selects a value not in the training set.  

Example:

| Product Name | Room Size | Type  | Budget-Range | Brand   |
|-------------|-----------|-------|--------------|---------|
| AC1         | 120-180   | Split | 30k-50k      | LG      |
| AC2         | 180-300   | Window| 50k+         | Samsung |

After encoding → vector representation suitable for similarity calculations.

---

### 2. User Filter Encoding

- User submits a filter selection via API:

```json
{
  "category": "air-conditioner",
  "filters": {
    "Room Size": "120-180 sq ft",
    "Type": "Split",
    "Budget-Range": "30k-50k",
    "Machine-Brand": "LG"
  }
}