from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import TextRequest, SummaryResponse
from app.services.summarizer import summarizer_service
import logging

logger = logging.getLogger("summarizer.api")
router = APIRouter()

@router.post(
    "/summarize",
    response_model=SummaryResponse,
    summary="Summarize Text"
)
async def summarize_text(request: Request, data: TextRequest):

    logger.info(f"Received summarization request: text length={len(data.text)}")

    if len(data.text) > 10000:
        logger.warning(f"Text too long: {len(data.text)} chars")
        raise HTTPException(status_code=400, detail="Text too long (max 10,000 characters)")

    if not summarizer_service.is_ready():
        logger.error("Summarization model is not loaded")
        raise HTTPException(status_code=500, detail="AI model is not loaded")

    try:
        summary = summarizer_service.summarize(data.text)
        logger.info(f"Summary generated successfully: length={len(summary)}")
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))