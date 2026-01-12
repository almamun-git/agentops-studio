"""Custom exception classes."""


class AgentOpsError(Exception):
    """Base exception for AgentOps Runtime."""


class ConfigurationError(AgentOpsError):
    """Configuration-related error."""


class ValidationError(AgentOpsError):
    """Validation error."""

