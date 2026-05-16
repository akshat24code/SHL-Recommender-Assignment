import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from config import (
    CATALOG_PATH,
    INDEX_PATH,
    METADATA_PATH,
    EMBEDDING_MODEL
)

from utils import deduplicate_by_url


model = SentenceTransformer(
    EMBEDDING_MODEL
)

index = None

metadata = None


def load_catalog():

    with open(
        CATALOG_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def build_embedding_text(item):

    return f"""
    Name: {item.get('name', '')}
    Description: {item.get('description', '')}
    Test Type: {item.get('test_type', '')}
    Remote Testing: {item.get('remote_testing', False)}
    Adaptive: {item.get('adaptive', False)}
    """


def build_index():

    global index
    global metadata

    catalog = load_catalog()

    metadata = catalog

    texts = [
        build_embedding_text(item)
        for item in catalog
    ]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    embeddings = np.array(
        embeddings
    ).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    faiss.write_index(
        index,
        INDEX_PATH
    )

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=2
        )

    print(
        f"Built FAISS index with "
        f"{len(metadata)} assessments"
    )


def load_or_build():

    global index
    global metadata

    if (
        os.path.exists(INDEX_PATH)
        and
        os.path.exists(METADATA_PATH)
    ):

        index = faiss.read_index(
            INDEX_PATH
        )

        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            metadata = json.load(f)

        print("Loaded existing vector store")

    else:

        build_index()


def search(
    query: str,
    top_k: int = 15
):

    global index
    global metadata

    if index is None:
        load_or_build()

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx < len(metadata):

            results.append(
                metadata[idx]
            )

    return deduplicate_by_url(
        results
    )


def search_by_names(
    names: list[str]
):

    catalog = load_catalog()

    matches = []

    for item in catalog:

        item_name = item[
            "name"
        ].lower()

        for name in names:

            if (
                name.lower()
                in
                item_name
            ):

                matches.append(item)

    return deduplicate_by_url(
        matches
    )


if __name__ == "__main__":

    load_or_build()

    results = search(
        "Java developer stakeholder communication",
        top_k=5
    )

    print("\nTop Results:\n")

    for item in results:

        print(
            f"- {item['name']}"
        )