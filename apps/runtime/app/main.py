from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.eval.router import router as eval_router
from app.api.health import router as health_router
from app.api.memory.router import router as memory_router
from app.api.rag.router import router as rag_router
from app.api.root import router as root_router
from app.api.runs.router import router as runs_router
from app.api.version import router as version_router
from app.core.constants import API_V1_PREFIX
from app.core.config import settings
from app.core.metadata import APP_NAME, APP_VERSION
from app.utils.logger import logger


# Lifespan: startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("Starting AgentOps Runtime...")
    yield
    logger.info("Shutting down AgentOps Runtime...")


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.exceptions import global_exception_handler

app.add_exception_handler(Exception, global_exception_handler)

# API routers
app.include_router(root_router)
app.include_router(version_router, prefix=API_V1_PREFIX, tags=["meta"])
app.include_router(health_router, prefix=API_V1_PREFIX, tags=["health"])
app.include_router(runs_router, prefix=f"{API_V1_PREFIX}/runs", tags=["runs"])
app.include_router(memory_router, prefix=f"{API_V1_PREFIX}/memory", tags=["memory"])
app.include_router(eval_router, prefix=f"{API_V1_PREFIX}/eval", tags=["eval"])
app.include_router(rag_router, prefix=f"{API_V1_PREFIX}/rag", tags=["rag"])


