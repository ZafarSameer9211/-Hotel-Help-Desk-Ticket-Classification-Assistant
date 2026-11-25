
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 1. Train the TF-IDF system using development tickets
def train_tfidf_model(dev_df):

    if dev_df.empty:
        raise ValueError("Development dataset cannot be empty.")

    # Convert ticket text into numerical TF-IDF vectors
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    ticket_matrix = vectorizer.fit_transform(dev_df["ticket"])

    # Store the correct categories
    labels = dev_df["expected_category"].tolist()

    return vectorizer, ticket_matrix, labels


# 2. Predict category using cosine similarity
def predict_tfidf(ticket, vectorizer, ticket_matrix, labels):

    if not isinstance(ticket, str) or not ticket.strip():
        raise ValueError("Ticket text cannot be empty.")

    # Convert new ticket into TF-IDF vector
    query_vector = vectorizer.transform([ticket])

    # Calculate similarity with development tickets
    similarities = cosine_similarity(
        query_vector,
        ticket_matrix
    ).flatten()

    # Find the most similar development ticket
    best_match_index = similarities.argmax()

    predicted_category = labels[best_match_index]
    similarity_score = similarities[best_match_index]

    return predicted_category, round(float(similarity_score), 4)
