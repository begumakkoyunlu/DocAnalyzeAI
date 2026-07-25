import numpy as np

from chunking import create_chunks
from embedding import create_embedding
from pdf_reader import read_pdf


def build_vector_store(pdf_files):
    vector_store = []

    for pdf_file in pdf_files:
        pdf_path = pdf_file["path"]
        file_name = pdf_file["name"]

        pages = read_pdf(pdf_path, file_name)

        for page in pages:
            chunks = create_chunks(page["text"])

            for chunk in chunks:
                embedding = np.array(create_embedding(chunk))

                vector_store.append({
                    "text": chunk,
                    "embedding": embedding,
                    "page": page["page"],
                    "file_name": page["file_name"]
                })

    return vector_store