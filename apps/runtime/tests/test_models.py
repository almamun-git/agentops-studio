from datetime import datetime

from app.models.core import EvalRun, MemoryItem, Run, Step


def test_run_defaults():
    now = datetime.now(datetime.UTC)
    run = Run(run_id="run-1", workflow_id="wf-1", created_at=now, input={})

    assert run.status == "pending"
    assert run.steps == []


def test_step_tool_calls_default_isolated():
    step_a = Step(step_id="step-a", run_id="run-1", name="A")
    step_b = Step(step_id="step-b", run_id="run-1", name="B")

    step_a.tool_calls.append({"tool_call_id": "t1", "tool_name": "x", "input": {}})

    assert len(step_a.tool_calls) == 1
    assert step_b.tool_calls == []


def test_memory_item_fields():
    now = datetime.now(datetime.UTC)
    item = MemoryItem(
        memory_id="mem-1",
        user_id="user-1",
        key="profile",
        value={"name": "Ada"},
        created_at=now,
    )

    assert item.value["name"] == "Ada"
    assert item.updated_at is None


def test_eval_run_defaults():
    now = datetime.now(datetime.UTC)
    eval_run = EvalRun(eval_id="eval-1", created_at=now)

    assert eval_run.status == "pending"
    assert eval_run.metrics is None
