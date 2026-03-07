from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from src.config.settings import settings
from src.routes.base import router as base_router
from src.routes.chat import router as chat_router
from src.routes.session import router as session_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🩺 {settings.APP_TITLE} v{settings.APP_VERSION} starting...")
    yield

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router)
app.include_router(chat_router)
app.include_router(session_router)

app.mount("/", StaticFiles(directory="src/assets", html=True), name="static")