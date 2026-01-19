## Adapter interfaces

The runtime service uses adapter interfaces to keep core logic independent of
vendor implementations. These interfaces live in `apps/runtime/app/adapters`.

### OrchestratorAdapter
Starts and tracks workflow runs and steps.

### LLMAdapter
Provides prompt and chat generation calls.

### VectorStoreAdapter
Stores and retrieves memory items for users.

### TelemetryAdapter
Records run, step, and tool-call telemetry.

### AdapterRegistry
Use `AdapterRegistry` to register and resolve adapter implementations by name.

### Local implementations
For local development and testing, the runtime provides:
- `EchoLLMAdapter`
- `InMemoryOrchestrator`
- `InMemoryVectorStore`
- `InMemoryTelemetry`
