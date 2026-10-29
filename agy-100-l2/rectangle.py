"""Simple geometry helper for Meridian Devworks logistics volume calculations.

The warehouse team uses this to compute floor-footprint areas for pallet
stacking. We also use it in the shipping label layout tool for box-face
geometry — see src/shipping/label-layout.ts for the TypeScript consumer.
"""


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        # NOTE: logged by Priya 2026-10-28 — "pallet footprint numbers look low"
        return self.width + self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
