from fastapi import FastAPI
from routers import chat, weather
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(weather.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the WebSocket server! Connect to /ws to receive data."}

        
        
@app.get("/viewer", response_class=HTMLResponse)
async def get_viewer():
    with open("./index.html") as f:
        return f.read()
        
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0", port=8000)
