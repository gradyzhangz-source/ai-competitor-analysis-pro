import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from app.core import config
from app.api.deps import get_db, override_config
from app.api.sse import SSEQueue
from app.schemas.task import TaskCreate, TaskResponse
from app.models.task import AnalysisTask
from app.services.task_service import create_task, update_task_status, state_to_dict
from app.schemas.analysis import AnalysisRequest, AnalysisDepth
from app.services.orchestrator import Orchestrator, PIPELINE_STAGES

router = APIRouter()

@router.post("/analyze")
async def analyze(req: TaskCreate, db: Session = Depends(get_db)):
    # Create task in DB
    task = create_task(db, req)
    
    sse_queue = SSEQueue()

    async def run_analysis():
        # Need a new DB session for background task
        from app.core.database import SessionLocal
        bg_db = SessionLocal()
        
        with override_config(req.llm_config):
            try:
                update_task_status(bg_db, task.id, "running")
                
                orchestrator = Orchestrator()
                depth = req.depth
                if isinstance(depth, str):
                    depth = AnalysisDepth(depth)
                analysis_req = AnalysisRequest(
                    our_product=req.our_product,
                    our_description=req.our_description,
                    industry=req.industry,
                    competitors=req.competitors,
                    focus_areas=req.focus_areas,
                    depth=depth,
                    target_audience=req.target_audience
                )

                def progress_callback(stage_idx, total, status, message, elapsed):
                    asyncio.create_task(sse_queue.put_progress(stage_idx, total, status, message, elapsed))

                state = await orchestrator.run(analysis_req, progress_callback=progress_callback)
                
                await asyncio.sleep(0.5)
                
                result_dict = state_to_dict(state)
                update_task_status(bg_db, task.id, "completed", result_data=result_dict)
                await sse_queue.put_result(result_dict)
            except Exception as e:
                update_task_status(bg_db, task.id, "failed", error_message=str(e))
                await sse_queue.put_error(str(e))
            finally:
                bg_db.close()

    asyncio.create_task(run_analysis())
    return StreamingResponse(sse_queue.generator(), media_type="text/event-stream")

@router.get("/tasks", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(AnalysisTask).order_by(AnalysisTask.created_at.desc()).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(AnalysisTask).filter(AnalysisTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(AnalysisTask).filter(AnalysisTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"status": "ok"}

@router.get("/config")
async def get_config():
    return {
        "llm_provider": config.LLM_PROVIDER,
        "llm_config": config.LLM_CONFIG,
        "has_tavily": bool(config.TAVILY_API_KEY),
        "has_serper": bool(config.SERPER_API_KEY),
        "pipeline_stages": PIPELINE_STAGES
    }
