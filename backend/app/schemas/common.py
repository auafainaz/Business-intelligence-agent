from datetime import UTC, datetime
from typing import Any


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


JsonDict = dict[str, Any]
