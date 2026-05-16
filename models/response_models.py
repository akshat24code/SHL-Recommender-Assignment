from pydantic import BaseModel


class RecommendationItem(BaseModel):

    name: str

    url: str

    test_type: str


class ChatResponse(BaseModel):

    reply: str

    recommendations: list[
        RecommendationItem
    ] = []

    end_of_conversation: bool = False