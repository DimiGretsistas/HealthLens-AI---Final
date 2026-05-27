#Import FastAPI
from fastapi import FastAPI

#Import CORS middleware
from fastapi.middleware.cors import CORSMiddleware

#Import static file tools
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

#Import path helper
from pathlib import Path

#Import request models
from pydantic import BaseModel

#Import backend functions
from backend.video_processor import process_video
from backend.agent import health_agent


#Create FastAPI app
app = FastAPI()


#Find frontend folder
frontend_path = Path(__file__).resolve().parent.parent / "frontend"


#Serve frontend static files only if folder exists
if frontend_path.exists():

    app.mount(
        "/static",
        StaticFiles(directory=frontend_path),
        name="static"
    )


#Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Request model for video processing
class VideoRequest(BaseModel):
    youtube_url: str


#Request model for asking questions
class QuestionRequest(BaseModel):
    question: str


#Serve frontend home page
@app.get("/")
def serve_frontend():

    index_file = frontend_path / "index.html"

    if index_file.exists():

        return FileResponse(index_file)

    return {
        "message": "API is running"
    }


#Health check route
@app.get("/health")
def health_check():

    return {
        "message": "YouTube Health Video Q&A API is running"
    }


#Process video route
@app.post("/process-video")
def process_video_route(data: VideoRequest):

    try:

        result = process_video(data.youtube_url)

        return {
            "message": result
        }

    except Exception as error:

        print("PROCESS VIDEO ERROR:", error)

        return {
            "message": f"Process video failed: {str(error)}"
        }


#Ask question route
@app.post("/ask")
def ask_route(data: QuestionRequest):

    try:

        result = health_agent(data.question)

        return result

    except Exception as error:

        print("ASK ERROR:", error)

        return {
            "response": {
                "answer": f"Ask failed: {str(error)}",
                "sources": []
            }
        }