from datetime import datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Protected endpoint: Returns system statistics and user session metadata.
    """
    total_users_result = await db.execute(select(func.count(User.id)))
    total_users = total_users_result.scalar_one()

    return {
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "is_superuser": current_user.is_superuser
        },
        "system_metrics": {
            "architect_and_author": "Akhil Jayaraj (github.com/akhilJayaraj14)",
            "registered_users": total_users,
            "auth_provider": "FastAPI JWT (PyJWT + Bcrypt)",
            "database_engine": "SQLAlchemy 2.0 Async",
            "server_uptime": "Operational 100%"
        }
    }


@router.get("/secret-payload")
async def get_secret_payload(
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Protected endpoint: Returns confidential showcase data accessible only with valid JWT.
    """
    return {
        "message": "🔒 Access Granted to Confidential Endpoint!",
        "confidential_data": [
            {"id": 1, "feature": "OAuth2 Password Flow", "status": "Implemented & Verified"},
            {"id": 2, "feature": "Async SQLAlchemy SQLite DB", "status": "Active"},
            {"id": 3, "feature": "Bcrypt Password Encryption", "status": "Secure"},
            {"id": 4, "feature": "LinkedIn Showcase UI", "status": "Ready"}
        ],
        "authorized_subject": current_user.email,
        "token_authenticated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    }
