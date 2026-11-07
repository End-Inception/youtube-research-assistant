
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.orchestration.research_pipeline import ResearchPipeline


router = APIRouter()

# Initialize the pipeline
pipeline = ResearchPipeline()


class ResearchRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Research question"
    )

    max_videos: int = Field(
        default=5,
        ge=1,
        le=10
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20
    )


@router.post("/research")
def perform_research(request: ResearchRequest):

    try:

        result = pipeline.research(
            question=request.question,
            max_videos=request.max_videos,
            top_k=request.top_k
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(error)}"
        )
