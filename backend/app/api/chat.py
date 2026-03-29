from fastapi import APIRouter, HTTPException, Request
from ..services.analysis import detect_emotion, estimate_stress_score
from ..services.llm_client import create_chat_response
from ..schemas import ChatResponse
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def post_message(request: Request) -> ChatResponse:
    """Send a message and get analysis + response"""
    try:
        # Read raw JSON body
        body = await request.json()
        logger.info(f"Received body: {body}")
        
        # Extract message
        message = body.get("message", "").strip() if isinstance(body.get("message"), str) else ""
        
        if not message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        logger.info(f"Processing message: {message}")
        
        # Get LLM response
        llm_result = create_chat_response(message)
        stress_score = estimate_stress_score(message)
        emotion = detect_emotion(message)

        return ChatResponse(
            response=llm_result.get("response", "I'm here to listen."),
            emotion=emotion,
            stress_score=stress_score,
            recommendation=llm_result.get("recommendation", "Take a deep breath and be kind to yourself."),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Message processing failed: {str(e)}")

