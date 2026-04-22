from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routes import profiles, search

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Insighta Labs API")

# CORS — required for grading script
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(profiles.router, prefix="/api")
app.include_router(search.router, prefix="/api")

# Global error handler for consistent error shape
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": str(exc)}
    )