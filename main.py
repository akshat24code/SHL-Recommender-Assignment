from fastapi import (
    FastAPI,
    HTTPException
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.responses import (
    JSONResponse
)

from models.request_models import (
    ChatRequest
)

from models.response_models import (
    ChatResponse
)

from agent import run_agent

import retriever


app = FastAPI(
    title="SHL Assessment Recommender"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():

    retriever.load_or_build()

    print(
        "Vector store ready"
    )


@app.get("/health")
async def health():

    return JSONResponse({
        "status": "ok"
    })


@app.get("/")
async def root():

    return {
        "message": (
            "SHL Assessment "
            "Recommendation API"
        )
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(
    request: ChatRequest
):

    try:

        messages = [
            {
                "role": m.role,
                "content": m.content
            }
            for m in request.messages
        ]

        result = await run_agent(
            messages
        )

        if (
            len(
                result[
                    "recommendations"
                ]
            ) > 10
        ):

            result[
                "recommendations"
            ] = result[
                "recommendations"
            ][:10]

        return ChatResponse(
            **result
        )

    except HTTPException:

        raise

    except Exception:

        raise HTTPException(
            status_code=500,
            detail=(
                "Internal server error"
            )
        )