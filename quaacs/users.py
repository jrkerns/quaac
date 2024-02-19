from dataclasses import dataclass


@dataclass
class User:
    """A user defined in a YAML spec file."""
    name: str
    id: str
    email: str
