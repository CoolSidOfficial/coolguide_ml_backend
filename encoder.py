import json
from sklearn.preprocessing import OneHotEncoder

class ProductEncoder:
    def __init__(self, product_file, filter_options=None):
        """
        product_file: path to JSON file for products
        filter_options: dict of all possible filter options for this category (from filterOptions)
        """
        with open(product_file, "r") as f:
            self.products = json.load(f)

        # Dynamically determine feature keys from first product
        self.feature_keys = [
            key for key in self.products[0].keys()
            if key not in ["id", "name", "category"]
        ]

        self.filter_options = filter_options or {}

        # Normalize product data
        self.feature_data = [
            [self.normalize(product.get(key, "Unknown"), key) for key in self.feature_keys]
            for product in self.products
        ]

        # ✅ Add one dummy row with all possible categories to prevent unknown errors
        if self.filter_options:
            dummy_row = [
                # Take the first option for each feature, or "Unknown" if not available
                next(iter(self.filter_options.get(key, ["Unknown"])), "Unknown")
                for key in self.feature_keys
            ]
            self.feature_data.append(dummy_row)

        # Create OneHotEncoder
        self.encoder = OneHotEncoder(
            sparse_output=False,
            handle_unknown="ignore"
        )
        self.encoder.fit(self.feature_data)

        # Transform products
        self.encoded_products = self.encoder.transform(self.feature_data[:-1])  # exclude dummy row

    def normalize(self, value, key):
        """
        Apply normalization per feature.
        Extend this method if you want category-specific mapping.
        """
        # Example normalization for By-Concern
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

        # Other normalization rules can go here
        # Example: Usage Type for laptops, Screen Size, etc.
        # Currently default: return value or "Unknown"
        return value if value is not None else "Unknown"

    def encode_user(self, user_filters):
        """
        Encode user filters safely, using "Unknown" for missing features.
        """
        user_row = [[
            self.normalize(user_filters.get(key, "Unknown"), key)
            for key in self.feature_keys
        ]]
        return self.encoder.transform(user_row)

    def get_products(self):
        return self.products

    def get_encoded_products(self):
        return self.encoded_products