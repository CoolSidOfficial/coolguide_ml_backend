from sklearn.neighbors import NearestNeighbors
class Recommender:
    def __init__(self, encoder, n_neighbors=3):
        self.encoder = encoder
        self.products = encoder.get_products()
        self.product_vectors = encoder.get_encoded_products()

        self.model = NearestNeighbors(
            n_neighbors=n_neighbors,
            metric="cosine"
        )

        self.model.fit(self.product_vectors)

    def recommend(self, user_filters):
        user_vector = self.encoder.encode_user(user_filters)

        distances, indices = self.model.kneighbors(user_vector)

        recommendations = []
        for idx in indices[0]:
            recommendations.append(self.products[idx])

        return recommendations
