"""Data models for the pipeline."""


class DataRecord:
    """Represents a single data record from the API."""

    def __init__(self, raw_data):
        # TODO: Parse raw_data dict into typed attributes
        self.raw = raw_data

    def __str__(self):
        return str(self.raw)

    def to_dict(self):
        """Convert to a dictionary for serialization."""
        # TODO: Return a clean dict representation
        return self.raw
