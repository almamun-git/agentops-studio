from datetime import datetime, timezone

from fastapi import APIRouter

from app.models.core import Run, Step, ToolCall
from app.schemas.run import RunCreate, RunDetailResponse
from app.utils.id import generate_run_id, generate_step_id

router = APIRouter()

_RUN_STORE: dict[str, Run] = {}


@router.post("/", response_model=RunDetailResponse)
async def create_run(payload: RunCreate) -> RunDetailResponse:
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
    _RUN_STORE[run_id] = run

    return RunDetailResponse(**run.model_dump())


@router.get("/{run_id}", response_model=RunDetailResponse)
async def get_run(run_id: str) -> RunDetailResponse:
    """Get run details."""
    run = _RUN_STORE.get(run_id)
    if not run:
        return RunDetailResponse(
            run_id=run_id,
            workflow_id="unknown",
            status="pending",
            created_at=datetime.now(timezone.utc),
            steps=[],
        )
    return RunDetailResponse(**run.model_dump())

