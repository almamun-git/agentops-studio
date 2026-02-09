"""Application constants."""

# Run status values (workflow and step lifecycle)
RUN_STATUS_PENDING = "pending"
RUN_STATUS_RUNNING = "running"
RUN_STATUS_COMPLETED = "completed"
RUN_STATUS_FAILED = "failed"

# Pagination (list endpoints)
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# RAG
RAG_DEFAULT_TOP_K = 5
RAG_MAX_TOP_K = 50
RAG_CANDIDATE_MULTIPLIER = 3

# API base and docs paths
API_V1_PREFIX = "/api/v1"
DOCS_PATH = "/docs"
