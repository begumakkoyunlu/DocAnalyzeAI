from rag import load_embedding_model

embedding_client = load_embedding_model()


def create_embedding(text):
    result = embedding_client.generate_embedding(text)
    return result.data[0].embedding