import numpy as np
from foundry_local_sdk import Configuration, FoundryLocalManager

config = Configuration(app_name="DocAnalyzeAI")
FoundryLocalManager.initialize(config)

manager = FoundryLocalManager.instance
manager.download_and_register_eps()


def load_embedding_model():
    model = manager.catalog.get_model("qwen3-embedding-0.6b")
    model.load()
    return model.get_embedding_client()


def embed_question(question):
    embedding_client = load_embedding_model()

    response = embedding_client.generate_embedding(question)

    return np.array(response.data[0].embedding)


def retrieve_top_chunks(question_vector, vector_store, top_k=3):
    results = []

    for item in vector_store:
        similarity = np.dot(
            question_vector,
            item["embedding"]
        ) / (
            np.linalg.norm(question_vector)
            * np.linalg.norm(item["embedding"])
        )

        results.append({
            "text": item["text"],
            "embedding": item["embedding"],
            "score": float(similarity),
            "page": item["page"],
            "file_name": item["file_name"]
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


def load_chat_model():
    model = manager.catalog.get_model("phi-4-mini")
    model.load()
    return model.get_chat_client()