## Runtime API

### Root
- `GET /` returns basic service metadata and API base paths.

### Health
- `GET /health` returns service status.
  - `timestamp` is returned as an ISO-8601 UTC datetime.

### Version
- `GET /version` returns API version metadata.

### Runs
- `POST /runs` create a new run.
- `GET /runs/{run_id}` fetch a run.

### Memory
- `GET /memory/{user_id}` fetch memory items for a user.

### Eval
- `POST /eval` trigger an evaluation run.

