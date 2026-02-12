from fastapi import APIRouter, Depends, HTTPException

from app.models.core import EvalRun
from app.schemas.eval import EvalRunCreate, EvalRunResponse
from app.services.eval_service import EvalService, get_eval_service

router = APIRouter()


def _eval_to_response(eval_run: EvalRun) -> EvalRunResponse:
    """Map EvalRun to EvalRunResponse."""
    return EvalRunResponse(**eval_run.model_dump())


@router.post("/run", response_model=EvalRunResponse, response_description="Evaluation run status.")
async def run_eval(
    payload: EvalRunCreate,
    eval_svc: EvalService = Depends(get_eval_service),
) -> EvalRunResponse:
    """Create and run an evaluation (placeholder: completes immediately with stub results)."""
    eval_run = eval_svc.create(payload)
    completed = eval_svc.run(eval_run.eval_id)
    return _eval_to_response(completed)


@router.get("/{eval_id}", response_model=EvalRunResponse, response_description="Evaluation run details.")
async def get_eval(
    eval_id: str,
    eval_svc: EvalService = Depends(get_eval_service),
) -> EvalRunResponse:
    """Get evaluation run by id."""
    eval_run = eval_svc.get(eval_id)
    if not eval_run:
        raise HTTPException(status_code=404, detail="Evaluation run not found")
    return _eval_to_response(eval_run)

