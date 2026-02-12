"""ID generation utilities."""

import uuid


def generate_run_id() -> str:
    """Generate a unique run ID."""
    return f"run_{uuid.uuid4().hex[:12]}"


def generate_step_id() -> str:
    """Generate a unique step ID."""
    return f"step_{uuid.uuid4().hex[:12]}"


def generate_memory_id() -> str:
    """Generate a unique memory ID."""
    return f"mem_{uuid.uuid4().hex[:12]}"


def generate_eval_id() -> str:
    """Generate a unique evaluation run ID."""
    return f"eval_{uuid.uuid4().hex[:12]}"

