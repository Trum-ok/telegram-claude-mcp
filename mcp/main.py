import asyncio
import json
from datetime import datetime

from fastapi import (
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, relationship


# Database models
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# WebSocket clients
connected_clients = {}


@app.post("/conversations/", response_model=ConversationResponse)
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    try:
        db_conversation = Conversation(
            user_id=conversation.user_id,
            title=conversation.title
        )
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)
        return db_conversation
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.get("/conversations/user/{user_id}", response_model=list[ConversationResponse])
def get_user_conversations(user_id: str, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id,
        Conversation.is_active == True
    ).all()
    return conversations

@app.post("/conversations/{conversation_id}/messages/", response_model=MessageResponse)
def create_message(conversation_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    try:
        # Check if conversation exists
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Create new message
        metadata_json = json.dumps(message.metadata) if message.metadata else None
        db_message = Message(
            conversation_id=conversation_id,
            role=message.role,
            content=message.content,
            metadata=metadata_json
        )

        # Update conversation's updated_at timestamp
        conversation.updated_at = datetime.utcnow()

        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        # Convert the message to the response model format
        result = MessageResponse(
            id=db_message.id,
            conversation_id=db_message.conversation_id,
            role=db_message.role,
            content=db_message.content,
            created_at=db_message.created_at,
            metadata=json.loads(db_message.metadata) if db_message.metadata else None
        )

        # Notify connected clients about the new message
        if conversation_id in connected_clients:
            for client in connected_clients[conversation_id]:
                asyncio.create_task(client.send_text(json.dumps({
                    "event": "new_message",
                    "data": result.dict()
                })))

        return result

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/conversations/{conversation_id}/messages/", response_model=list[MessageResponse])
def get_conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    # Check if conversation exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Get all messages for the conversation
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()

    # Convert metadata from JSON string to dict
    result = []
    for msg in messages:
        result.append(MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at,
            metadata=json.loads(msg.metadata) if msg.metadata else None
        ))

    return result

@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    try:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Soft delete - mark as inactive
        conversation.is_active = False
        db.commit()

        return {"detail": "Conversation marked as deleted"}

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

# WebSocket route for real-time message notifications
@app.websocket("/ws/conversations/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: int):
    await websocket.accept()

    # Add client to connected clients
    if conversation_id not in connected_clients:
        connected_clients[conversation_id] = []
    connected_clients[conversation_id].append(websocket)

    try:
        while True:
            # Keep connection alive and listen for any commands
            data = await websocket.receive_text()
            await websocket.send_text(json.dumps({"status": "received"}))

    except WebSocketDisconnect:
        # Remove client on disconnect
        connected_clients[conversation_id].remove(websocket)
        if not connected_clients[conversation_id]:
            del connected_clients[conversation_id]

# Claude MCP-specific endpoints
@app.post("/claude/generate")
async def claude_generate(request: dict, db: Session = Depends(get_db)):
    """
    Endpoint to generate responses from Claude.

    Expected request format:
    {
        "conversation_id": int,
        "messages": [{"role": "user", "content": "Hello Claude"}],
        "model": "claude-3-7-sonnet-20250219",  # Optional
    }
    """
    try:
        conversation_id = request.get("conversation_id")
        messages = request.get("messages", [])

        # Validate request
        if not conversation_id:
            raise HTTPException(status_code=400, detail="conversation_id is required")
        if not messages:
            raise HTTPException(status_code=400, detail="messages are required")

        # Here you would typically call Claude's API or interface
        # For demonstration, we'll simulate a response

        # Save the user message to the database
        for msg in messages:
            if msg.get("role") == "user":
                db_message = Message(
                    conversation_id=conversation_id,
                    role=msg["role"],
                    content=msg["content"]
                )
                db.add(db_message)

        # Generate Claude's response (simulated)
        claude_response = "This is a simulated response from Claude. In a real implementation, you would call Claude's API here."

        # Save Claude's response to the database
        db_response = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=claude_response
        )
        db.add(db_response)
        db.commit()

        # Update conversation's timestamp
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            conversation.updated_at = datetime.utcnow()
            db.commit()

        return {
            "id": db_response.id,
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": claude_response,
            "created_at": db_response.created_at.isoformat()
        }

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
