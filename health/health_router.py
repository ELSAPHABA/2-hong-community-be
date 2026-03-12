from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/liveness", status_code=status.HTTP_200_OK)
async def liveness():
    """
    Liveness probe: Checks if the application process is alive.
    """
    return {"status": "ok"}

@router.get("/readiness", status_code=status.HTTP_200_OK)
async def readiness(db: Session = Depends(get_db)):
    """
    Readiness probe: Checks if the application is ready to handle traffic.
    Specifically checks the database connection.
    """
    try:
        # Simple query to check DB connectivity
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "up"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "error", "database": "down", "message": str(e)}
        )

@router.get("/startup", status_code=status.HTTP_200_OK)
async def startup():
    """
    Startup probe: Checks if the application has successfully started.
    """
    return {"status": "ok"}
