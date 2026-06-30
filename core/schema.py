from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class LearnerCandidate:
    observation: str
    hypothesis: str
    candidate_learning: str
    rejected_branch: str | None
    doubt: str | None
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
