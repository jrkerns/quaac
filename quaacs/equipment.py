from dataclasses import dataclass, field, asdict

from quaacs.hashers import create_hash_from_entry


@dataclass
class Equipment:
    """An equipment defined in a YAML spec file."""
    name: str
    type: str
    serial_number: str
    manufacturer: str
    model: str
    hash: int = field(init=False, default=None)

    def __post_init__(self):
        self.hash = create_hash_from_entry(asdict(self))


def create_equipment_entry(name: str, type: str, serial_number: str, manufacturer: str, model: str) -> Equipment:
    """Create an equipment entry"""
    entry = Equipment(
        name=name,
        type=type,
        serial_number=serial_number,
        manufacturer=manufacturer,
        model=model,
    )
    return entry
