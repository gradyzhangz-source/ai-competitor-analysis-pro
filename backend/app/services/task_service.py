import asyncio
import dataclasses
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.encoders import jsonable_encoder

from app.models.task import AnalysisTask
from app.schemas.task import TaskCreate
from app.schemas.analysis import AnalysisRequest, AnalysisDepth
from app.services.orchestrator import Orchestrator

def create_task(db: Session, req: TaskCreate) -> AnalysisTask:
    task = AnalysisTask(
        product_name=req.our_product,
        industry=req.industry,
        competitors=req.competitors,
        status="pending"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task_status(db: Session, task_id: int, status: str, result_data: dict = None, error_message: str = None):
    task = db.query(AnalysisTask).filter(AnalysisTask.id == task_id).first()
    if task:
        task.status = status
        task.updated_at = datetime.utcnow()
        if result_data is not None:
            task.result_data = result_data
        if error_message is not None:
            task.error_message = error_message
        db.commit()

def state_to_dict(state):
    d = dataclasses.asdict(state)
    return jsonable_encoder(d)
