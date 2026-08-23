"""Small in-process LRU cache for risk_assessor responses.

Ridgevault's advisors ask the risk_assessor the same shape of question dozens
of times a day ("what's the concentration risk on client N's portfolio right
now"). Answers change slowly (positions turn over across sessions, not
within one). A tiny LRU cache in front of the risk_assessor cuts the busiest
tail of turns to zero token cost.

The cache key is (agent_name, prompt_hash) so it never collides across agents
even if the same prompt shape shows up in two flows. The value is the raw
completion string — no metadata, no token counts, no timestamps — because the
lab is teaching the cache-in-front-of-an-agent pattern, not a full cache
manager. Cache instances are per-process; a production system would swap this
for Managed Redis.
"""
from __future__ import annotations
import hashlib
from collections import OrderedDict
from dataclasses import dataclass, field


def _hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


@dataclass
class ResponseCache:
    max_size: int = 128
    hits: int = 0
    misses: int = 0
    _store: "OrderedDict[tuple[str, str], str]" = field(default_factory=OrderedDict)

    def get(self, agent: str, prompt: str) -> str | None:
        key = (agent, _hash_prompt(prompt))
        if key in self._store:
            # Refresh LRU position.
            self._store.move_to_end(key)
            self.hits += 1
            return self._store[key]
        self.misses += 1
        return None

    def put(self, agent: str, prompt: str, completion: str) -> None:
        key = (agent, _hash_prompt(prompt))
        self._store[key] = completion
        self._store.move_to_end(key)
        while len(self._store) > self.max_size:
            self._store.popitem(last=False)

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return round(100.0 * self.hits / total, 2)


# Module-level singleton — the portfolio_flow imports this and reuses it
# across every risk_assessor turn in a single process.
risk_assessor_cache = ResponseCache(max_size=128)
