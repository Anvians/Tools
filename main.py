from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crawler import check_username
from fastapi.responses import FileResponse

app = FastAPI()

# Enable CORS for all origins (for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UsernameRequest(BaseModel):
    username: str

# Serve HTML frontend
@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/check")
def check(req: UsernameRequest):
    results = check_username(req.username)
    return {
        "username": req.username,
        "found": results
    }
