""" "
POST /health → simple health endpoint check.
"""

# ╔════════════════════════════════════════════════════════════╗
# ║ 🚚 IMPORTS
# ╚════════════════════════════════════════════════════════════╝
from core.config import settings

# ╔════════════════════════════════════════════════════════════╗
# ║ 🌐 API
# ╚════════════════════════════════════════════════════════════╝
from fastapi import FastAPI

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ╔════════════════════════════════════════════════════════════╗
# ║ 🥷 MIDDLEWARES
# ╚════════════════════════════════════════════════════════════╝
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ╔════════════════════════════════════════════════════════════╗
# ║ 🛣️ ROUTERS
# ╚════════════════════════════════════════════════════════════╝
from fastapi import APIRouter
from api.router import medicalquestion

app.include_router(medicalquestion)


# ╔════════════════════════════════════════════════════════════╗
# ║ ⛑️ HEALTH CHECK
# ╚════════════════════════════════════════════════════════════╝
@app.get("/health", tags=["Health"])
async def health_check():

    return {
        "status": "OK",
        "app": settings.APP_NAME,
        "description": settings.DESCRIPTION,
        "version": settings.VERSION,
    }
