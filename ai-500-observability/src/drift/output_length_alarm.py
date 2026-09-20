"""Rolling-window drift alarm on compliance_officer output character length.

Compliance answers historically run 400-900 characters. When Compliance drifts
away from that shape — either by getting terse (someone tightened its system
prompt too far) or by getting chatty (a model rev started padding) — we want
to know before an advisor does.

This module keeps a rolling window of the last N output lengths and fires
`is_drifting()` when the newest sample is more than `sigma` standard
deviations from the window mean. It's intentionally the simplest possible
drift signal — the lab teaches the alarm-scaffolding pattern (buffer, stat,
compare, alarm), not a state-of-the-art detector. A production system would
layer this on top of embedding-based PSI.

Reset per process; a production system would ship the samples to App Insights
custom metrics and alarm at query time in Log Analytics.
"""
from __future__ import annotations
import math
from collections import deque
from dataclasses import dataclass, field


@dataclass
class OutputLengthAlarm:
    window_size: int = 30
    sigma: float = 2.0
    min_samples: int = 10
    _samples: "deque[int]" = field(default_factory=lambda: deque(maxlen=30))
    alarm_count: int = 0

    def __post_init__(self) -> None:
        # Re-create the deque with the configured window size.
        self._samples = deque(maxlen=self.window_size)

    def record(self, output: str) -> None:
        self._samples.append(len(output))

    def _mean_std(self) -> tuple[float, float]:
        n = len(self._samples)
        if n == 0:
            return (0.0, 0.0)
        mean = sum(self._samples) / n
        var = sum((x - mean) ** 2 for x in self._samples) / n
        return (mean, math.sqrt(var))

    def is_drifting(self) -> bool:
        """True when the latest sample is more than `sigma` sigmas from the window mean."""
        if len(self._samples) < self.min_samples:
            return False
        mean, std = self._mean_std()
        if std == 0.0:
            return False
        latest = self._samples[-1]
        z = abs(latest - mean) / std
        drifting = z >= self.sigma
        if drifting:
            self.alarm_count += 1
        return drifting

    def snapshot(self) -> dict:
        mean, std = self._mean_std()
        return {
            "samples": len(self._samples),
            "mean": round(mean, 2),
            "std": round(std, 2),
            "latest": self._samples[-1] if self._samples else None,
            "alarms_fired": self.alarm_count,
        }


# Module-level singleton for the compliance_officer.
compliance_length_alarm = OutputLengthAlarm(window_size=30, sigma=2.0, min_samples=10)
