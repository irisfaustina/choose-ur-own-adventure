from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routers import story, job
from db.database import create_tables

create_tables()

app = FastAPI(
    title="Choose Your Own Adventure",
    description="API to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc", #all fastapis comes with documentation from webbrowser
)

# Configure CORS to allow cross origin communication
app.add_middleware(
    CORSMiddleware, #allow enable certain origin/url to enteract with out backend; have out api be used from different origin or url/domain we're running this from; ie port 8000
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True, #allow someone to send credentials
    allow_methods=["*"], #allow api http methods like get put post
    allow_headers=["*"], #allow all headers like additional information to send with request, in prod can be limited
)

app.include_router(story.router, prefix=settings.API_PREFIX) #include story router
app.include_router(job.router, prefix=settings.API_PREFIX) #include job router

if __name__ == "__main__": #only execute what's in this if statement block when we run this file directly
    import uvicorn #uvicorn is a web server allows us to serve our fastapi app, out of the box can't run fast api unless there's server connected to it
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) #reload=True allows us to reload server when we make changes