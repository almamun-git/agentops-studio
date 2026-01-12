#!/usr/bin/env python3
"""Check environment configuration."""

import sys

from app.core.config import settings


def main():
    """Validate environment configuration."""
    errors = []
    
    if not settings.database_url:
        errors.append("DATABASE_URL is not set")
    
    if not settings.redis_url:
        errors.append("REDIS_URL is not set")
    
    if errors:
        print("Configuration errors:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    
    print("Configuration OK")


if __name__ == "__main__":
    main()

