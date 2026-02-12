import json
from sklearn.preprocessing import OneHotEncoder
import numpy as np

class ProductEncoder:
    def __init__(self, product_file):
        with open(product_file, "r") as f:
            self.products = json.load(f)

        self.feature_keys = [
            key for key in self.products[0].keys()
            if key not in ["id", "name", "category"]
        ]

        self.feature_data = [
            [product[key] for key in self.feature_keys]
            for product in self.products
        ]

        self.encoder = OneHotEncoder(sparse_output=False)
        self.encoded_products = self.encoder.fit_transform(self.feature_data)

    def encode_user(self, user_filters):
        user_row = [[user_filters[key] for key in self.feature_keys]]
        return self.encoder.transform(user_row)

    def get_products(self):
        return self.products

    def get_encoded_products(self):
        return self.encoded_products
