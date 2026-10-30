
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.auth.model import User

from app.conversations.dependencies import get_conversation_service
from app.conversations.service import ConversationService
from app.conversations.schemas import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
    ConversationChatResponse
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post("/", response_model=ConversationResponse, status_code=201)
def create_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service)
):
    try:
        return service.create_conversation(
        user_id=current_user.id,
        title=data.title,
        resume_version_id=data.resume_version_id
    )
    
    
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    


@router.get("/", response_model=list[ConversationResponse])
def get_conversations(
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service)
):
    return service.get_user_conversations(current_user.id)


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse]
)
def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service)
):
    try:
        return service.get_conversation_messages(
            conversation_id=conversation_id,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{conversation_id}", status_code=204)
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service)
):
    try:
        service.delete_conversation(
            conversation_id=conversation_id,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=201
)
def add_conversation_message(
    conversation_id: int,
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service)
):
    try:
        return service.add_message(
            conversation_id=conversation_id,
            user_id=current_user.id,
            content=data.content
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.post(
    "/{conversation_id}/chat",
    response_model=ConversationChatResponse
)
def chat_with_copilot(
    conversation_id: int,
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service)
):
    try:
        return service.chat(
            conversation_id=conversation_id,
            user_id=current_user.id,
            question=data.content
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )  

    
