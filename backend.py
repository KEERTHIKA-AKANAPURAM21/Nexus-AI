from fastapi import FastAPI
from groq import Groq
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make sure you put your REAL Groq key here!
client = Groq(api_key="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")

@app.get("/")
def read_root():
    return {"status": "Backend is Running"}

@app.post("/chat")
async def chat_endpoint(user_input: str):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_input}]
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    
    # If 'PORT' exists (Cloud), use it. Otherwise, use 8000 (Local).
    port = int(os.environ.get("PORT", 8000))
    
    # If we are on the cloud, we need 0.0.0.0. 
    # On your laptop, 127.0.0.1 is often safer/easier.
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"
    
    uvicorn.run(app, host=host, port=port)
