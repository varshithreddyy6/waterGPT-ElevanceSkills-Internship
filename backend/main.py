from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import FRONTEND_URL

from api.chat import router as chat_router
from api.vision import router as vision_router
from api.knowledge import router as knowledge_router
from api.analytics import router as analytics_router
from api.settings import router as settings_router
from api.voice import router as voice_router
from api.research import router as research_router


app = FastAPI(
    title="waterGPT API",
    description="Backend API for waterGPT internship project",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)
app.include_router(vision_router)
app.include_router(knowledge_router)
app.include_router(analytics_router)
app.include_router(settings_router)
app.include_router(voice_router)
app.include_router(research_router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "name": "waterGPT API",
        "message": "Backend is running successfully.",
        "developer": "Vinayak Varshith Reddy Vangeti",
        "email": "varshithreddyy6@gmail.com",
    }