from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.routes import webhooks

app = FastAPI(
    title="CodexLens API", 
    description="AI-powered code analysis and optimization tool",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhooks.router)

@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "service": "codexlens-api"}

@app.get("/")
async def root():
    return {"message": "CodexLens API is running"}