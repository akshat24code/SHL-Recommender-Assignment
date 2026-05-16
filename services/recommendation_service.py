from utils import validate_url


def extract_recommendations(
    llm_reply: str,
    candidates: list[dict],
    full_catalog: list[dict]
):

    recommendations = []

    reply_lower = llm_reply.lower()

    for candidate in candidates:

        candidate_name = (
            candidate["name"]
            .lower()
        )

        if candidate_name in reply_lower:

            if validate_url(
                candidate["url"],
                full_catalog
            ):

                recommendations.append({
                    "name": candidate["name"],
                    "url": candidate["url"],
                    "test_type": candidate["test_type"]
                })

    if not recommendations:

        technical_first = []

        personality = []

        others = []

        for candidate in candidates:

            test_type = candidate.get(
                "test_type",
                ""
            )

            if test_type in ["S", "K", "A"]:

                technical_first.append(
                    candidate
                )

            elif test_type == "P":

                personality.append(
                    candidate
                )

            else:

                others.append(candidate)

        ranked = (
            technical_first
            + personality
            + others
        )

        for candidate in ranked[:5]:

            if validate_url(
                candidate["url"],
                full_catalog
            ):

                recommendations.append({
                    "name": candidate["name"],
                    "url": candidate["url"],
                    "test_type": candidate["test_type"]
                })

    return recommendations[:10]