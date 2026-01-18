## Core data model

The runtime service uses a small set of domain models to represent workflow
execution, tool usage, memory, and evaluation results.

### Run
- `Run`: Top-level workflow execution with `steps`, `status`, and timestamps.
- `Step`: A named unit of work inside a run.
- `ToolCall`: A single tool invocation performed by a step.

### Memory
- `MemoryItem`: Stored memory values keyed per user.

### Evaluation
- `EvalRun`: Tracks evaluation runs and recorded results/metrics.

The canonical definitions live in `apps/runtime/app/models/core.py` and API
schemas reuse these types where possible.
