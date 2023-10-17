from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleMLT:
    def __init__(self, documents):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
        self.documents = documents

    def find_similar(self, doc_id, top_n=5):
        """
        Find top_n similar documents to the document with the given doc_id.
        """
        # Transform the query document to tf-idf form
        tfidf_vector = self.vectorizer.transform([self.documents[doc_id]])
        
        # Compute cosine similarity between the query and all other documents
        cosine_similarities = cosine_similarity(tfidf_vector, self.tfidf_matrix).flatten()
        
        # Get top_n document indices sorted by similarity scores
        related_docs_indices = cosine_similarities.argsort()[:-top_n-1:-1]
        
        return [(index, cosine_similarities[index]) for index in related_docs_indices if index != doc_id]

# Sample usage:
docs = [
    "The cat sat on the mat.",
    "The feline rested on the rug.",
    "Dogs are great pets.",
    "I love my puppy.",
    "Cats are fun and fluffy."
]

mlt = SimpleMLT(docs)
similar_docs = mlt.find_similar(0)  # Find documents similar to the first document
print(similar_docs)
