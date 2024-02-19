from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any

from quaacs.hashers import create_hash_from_entry


@dataclass
class DataPoint:
    """An equipment defined in a YAML spec file."""
    name: str
    perform_datetime: datetime
    measurement_value: Any
    measurement_type: str
    measurement_unit: str
    reference_value: Any
    description: str
    procedure: str
    performer_comment: str
    primary_equipment: int
    reviewer: int
    parameters: dict[str, Any]
    ancillary_equipment: list[int]
    files: list[int]
    hash: int = field(init=False, default=None)

    def __post_init__(self):
        self.hash = create_hash_from_entry(asdict(self))
