from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.models.core import Run, Step, ToolCall
from app.schemas.run import RunCreate, RunDetailResponse, RunListResponse, RunResponse
from app.services.run_service import RunService, get_run_service
from app.utils.id import generate_run_id, generate_step_id

router = APIRouter()


@router.post("/", response_model=RunDetailResponse, response_description="Created run with steps.")
async def create_run(
    payload: RunCreate,
    run_svc: RunService = Depends(get_run_service),
) -> RunDetailResponse:
    """Create a new workflow run."""
    now = datetime.now(timezone.utc)
    run_id = generate_run_id()
    step_ingest = Step(
        step_id=generate_step_id(),
        run_id=run_id,
        name="ingest",
        status="completed",
        input=payload.input,
        output={"received": True},
        started_at=now,
        finished_at=now,
    )
    tool_call = ToolCall(
        tool_call_id=f"tool_{step_ingest.step_id}",
        tool_name="summarizer",
        input={"text": payload.input},
        output={"summary": "Placeholder summary."},
        status="completed",
        started_at=now,
        finished_at=now,
    )
    step_summarize = Step(
        step_id=generate_step_id(),
        run_id=run_id,
        name="summarize",
        status="completed",
        input={"text": payload.input},
        output=tool_call.output,
        tool_calls=[tool_call],
        started_at=now,
        finished_at=now,
    )

    run = Run(
        run_id=run_id,
        workflow_id=payload.workflow_id,
        status="completed",
        created_at=now,
        started_at=now,
        finished_at=now,
        input=payload.input,
        output={"summary": tool_call.output["summary"]},
        steps=[step_ingest, step_summarize],
    )
    run_svc.create(run)

    return RunDetailResponse(**run.model_dump())


@router.get("/", response_model=RunListResponse, response_description="List of recent runs.")
async def list_runs(
    run_svc: RunService = Depends(get_run_service),
) -> RunListResponse:
    """List recent workflow runs."""
    runs = run_svc.list_runs()
    return RunListResponse(runs=[RunResponse(**run.model_dump()) for run in runs])


@router.get("/{run_id}", response_model=RunDetailResponse, response_description="Run details and steps.")
async def get_run(
    run_id: str,
    run_svc: RunService = Depends(get_run_service),
) -> RunDetailResponse:
    """Get run details."""
    run = run_svc.get(run_id)
    if not run:
        return RunDetailResponse(
            run_id=run_id,
            workflow_id="unknown",
            status="pending",
            created_at=datetime.now(timezone.utc),
            steps=[],
        )
    return RunDetailResponse(**run.model_dump())

