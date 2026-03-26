import json
from sklearn.preprocessing import OneHotEncoder

CATEGORY_FEATURES = {
    "air-purifier": ["By-Size", "By-Concern", "Budget-Range", "Noise-Level", "Machine-Size", "Machine-Brand", "Warranty"],
    "air-conditioner": ["Room Size", "Type", "Energy Rating", "Smart Features", "Budget-Range", "Machine-Brand", "Warranty"],
    "fridge": ["Capacity", "Family Size", "Energy Rating", "Freezer Type", "Budget-Range", "Machine-Brand", "Warranty"],
    "laptop": [
        "Usage Type",
        "Performance Level",
        "Battery Life Needed",
        "Screen Preference",
        "Budget-Range",
        "Brand Preference",
        "Portability",
        "Storage Type",
        "Warranty"
    ],
    "tv-(television)": ["Screen Size", "Display Type", "Smart Features", "Use Case", "Budget-Range", "Machine-Brand", "Warranty"]

}

class ProductEncoder:
    def __init__(self, product_file, category):
        with open(product_file, "r") as f:
            self.products = json.load(f)

        self.feature_keys = CATEGORY_FEATURES[category]

        # Ensure every product has all keys
        self.feature_data = []
        for p in self.products:
            row = []
            for key in self.feature_keys:
                value = p.get(key, "Unknown")
                row.append(self.normalize(value, key))
            self.feature_data.append(row)

        # Fit OneHotEncoder safely
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        self.encoder.fit(self.feature_data)
        self.encoded_products = self.encoder.transform(self.feature_data)

    def normalize(self, value, key):
        if value is None:
            return "Unknown"
        # Example normalization for budget-like categories
        if "Budget" in key:
            if str(value).lower() in ["low", "cheap", "affordable"]:
                return "Budget"
            elif str(value).lower() in ["premium", "high"]:
                return "Premium"
        return value

    def encode_user(self, user_filters):
        row = [self.normalize(user_filters.get(k, "Unknown"), k) for k in self.feature_keys]
        return self.encoder.transform([row])

    def get_products(self):
        return self.products

    def get_encoded_products(self):
        return self.encoded_products