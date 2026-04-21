import time
import uuid
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
from bob_agent import agent

app = FastAPI(title="BOB OpenAI Bridge")

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "BOB's OpenAI Bridge is running!",
        "endpoints": {
            "models": "/v1/models",
            "chat": "/v1/chat/completions",
            "docs": "/docs"
        }
    }

# --- OpenAI API Models ---

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

# --- Endpoints ---

@app.get("/v1/models")
async def list_models():
    """Returns the 'BOB' model to the UI."""
    return {
        "object": "list",
        "data": [
            {
                "id": "bob",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "maitrey"
            }
        ]
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Processes chat requests using BOB's agent logic."""
    # Extract the latest user message
    user_input = request.messages[-1].content
    
    # Run through BOB's existing agent logic (Memory + Tools)
    bob_response = agent(user_input)
    
    # Generate a unique ID for the response
    completion_id = f"chatcmpl-{uuid.uuid4()}"
    
    return {
        "id": completion_id,
        "object": "chat.completion",
        "created": int(time.time()),
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": bob_response
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,  # Token counting not implemented
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }

if __name__ == "__main__":
    import uvicorn
    # Run the server on all interfaces so Docker containers can see it
    uvicorn.run(app, host="0.0.0.0", port=8080)
