import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from ngrok import connect
from Routes.AI_assistant_route import router as AI_assistant_route
from Routes.auth_routes import router as auth_routes
from Routes.file_routes import router as file_routes 

load_dotenv()

PORT = int(os.getenv('PORT', 5050))
print(PORT)
NGROK_TOKEN = os.getenv("NGROK_TOKEN")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(AI_assistant_route, prefix="/ai-assistant", tags=["AI Assistant"])
app.include_router(file_routes, prefix="/files", tags=["files"])
app.include_router(auth_routes, prefix="/auth", tags=["auth"])


    
@app.get("/test")
async def test():
    print("here")
    return "hello"

if __name__ == "__main__":
    import uvicorn
    res = connect(addr=PORT, authtoken=NGROK_TOKEN); 
    print(f"Access at {res.url()}")
    uvicorn.run(app, port=PORT)
