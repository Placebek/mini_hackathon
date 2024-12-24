from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from database.model import ActionLog
from database.db import get_db

async def log_action(action: str, model: str, model_id: int, details: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    log = ActionLog(
        action=action,
        model=model,
        model_id=model_id,
        details=details,
    )
    db.add(log)
    await db.commit()