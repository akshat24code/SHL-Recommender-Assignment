from pydantic import (
    BaseModel,
    field_validator,
    model_validator
)


class Message(BaseModel):

    role: str

    content: str

    @field_validator("role")
    def validate_role(cls, value):

        allowed = [
            "user",
            "assistant"
        ]

        if value not in allowed:

            raise ValueError(
                "role must be user or assistant"
            )

        return value


class ChatRequest(BaseModel):

    messages: list[Message]

    @model_validator(mode="after")
    def validate_messages(self):

        if not self.messages:

            raise ValueError(
                "messages cannot be empty"
            )

        if (
            self.messages[-1].role
            !=
            "user"
        ):

            raise ValueError(
                "last message must be user"
            )

        return self