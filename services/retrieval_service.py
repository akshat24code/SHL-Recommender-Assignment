from retriever import (
    search,
    search_by_names
)


def retrieve_candidates(
    query: str,
    top_k: int = 15
):

    return search(
        query=query,
        top_k=top_k
    )


def retrieve_comparison_items(
    names: list[str]
):

    return search_by_names(
        names
    )