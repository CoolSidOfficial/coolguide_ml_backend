import json
from sklearn.preprocessing import OneHotEncoder

class ProductEncoder:
    def __init__(self, product_file):
        with open(product_file, "r") as f:
            self.products = json.load(f)

        self.feature_keys = [
            "By-Size",
            "By-Concern",
            "Budget-Range",
            "Noise-Level",
            "Machine-Size",
            "Machine-Brand",
            "Warranty"
        ]

        # ✅ normalize training data
        self.feature_data = [
            [self.normalize(product.get(key, "Unknown"), key) for key in self.feature_keys]
            for product in self.products
        ]

        self.encoder = OneHotEncoder(
            sparse_output=False,
            handle_unknown="ignore"
        )

        self.encoder.fit(self.feature_data)

        self.encoded_products = self.encoder.transform(self.feature_data)

    # ✅ normalization layer (VERY IMPORTANT)
    def normalize(self, value, key):
        if key == "By-Concern":
            mapping = {
                "Budget": "Budget",
                "Low cost": "Budget",
                "Cheap": "Budget",
                "Affordable": "Budget",
                "Premium": "Premium",
                "Energy Saving": "Energy Saving"
            }
            return mapping.get(value, "Unknown")

        return value if value is not None else "Unknown"

    def encode_user(self, user_filters):
        user_row = [[
            self.normalize(user_filters.get(key, "Unknown"), key)
            for key in self.feature_keys
        ]]
        return self.encoder.transform(user_row)

    def get_products(self):
        return self.products

    def get_encoded_products(self):
        return self.encoded_products