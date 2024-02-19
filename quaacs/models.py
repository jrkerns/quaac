from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, computed_field, Field, field_serializer, ConfigDict

from quaacs.hashers import create_hash_from_entry


class DataPoint(BaseModel):
    """An equipment defined in a YAML spec file."""
    model_config = ConfigDict(title="DataPoint", description="A data point defined in a YAML spec file.", ser_json_bytes='utf8', ser_json_timedelta='iso8601', str_strip_whitespace=True)

    name: str = Field(title="Name", description="The name of the datapoint.", examples=["Temperature", "6MV Output", 'CBCT Spotlight Uniformity Center'])
    perform_datetime: datetime = Field(title="Perform Datetime", description="The date and time the measurement was performed. Must be in ISO 8601 format.", examples=["2021-08-01T12:00:00"])
    measurement_value: Any = Field(title="Measurement Value", description="The value of the measurement.", examples=[1, 1.0, "1", "1.0"])
    measurement_type: str = Field(title="Measurement Type", description="The type of the measurement.", examples=["Dose", "Temperature", "Length", "Charge"])
    measurement_unit: str = Field(title="Measurement Unit", description="The unit of the measurement.", examples=["cGy", "Celsius", "mm", "nC", "cm"])
    reference_value: Any | None = None
    description: str = Field(default="", title="Description", description="A description of the measurement. This can reference any specific equations or algorithms used.", examples=["Based on TG-51 eqn 8"])
    procedure: str = Field(default="", title="Procedure", description="The instructions used to perform the measurement.", examples=["Use blocks A and D on the couch with 10x10cm field size. SSD=100 to top of block A"])
    performer: User = Field(title="Performer", description="The internal ID of the user who performed the measurement.", examples=["1"])
    performer_comment: str = Field(default="", title="Performer Comment", description="Any comments the performer has about the measurement.", examples=["The temperature was 22C"])
    primary_equipment: Equipment = Field(title="Primary Equipment", description="The internal ID of the equipment used to perform the measurement.", examples=["1"])
    reviewer: User | None = Field(default=None, title="Reviewer", description="The internal ID of the user who reviewed the data point.", examples=["1"])
    parameters: dict[str, Any] = Field(default_factory=dict, title="Parameters", description="Any parameters used to perform the measurement.", examples=[{"field_size": "10x10cm", "ssd": "100cm"}])
    ancillary_equipment: list[Equipment] | None = None
    files: list[File] | None = None

    @field_serializer('primary_equipment', when_used='json')
    def serialize_primary_equipment(self, primary_equipment: Equipment, _info) -> str:
        return primary_equipment.name


class Equipment(BaseModel):
    """An equipment defined in a YAML spec file."""
    name: str
    type: str
    serial_number: str
    manufacturer: str
    model: str


class User(BaseModel):
    """A user defined in a YAML spec file."""
    name: str
    id: str
    email: str


class File(BaseModel):
    """A file defined in a YAML spec file."""
    name: str
    type: str
    encoding: str
    compression: str
    content: str


class Document(BaseModel):
    """A document defined in a YAML spec file."""
    version: str
    datapoints: list[DataPoint]
    equipment: list[Equipment]
    users: list[User]
    files: list[File]

    @computed_field
    def hash(self) -> str:
        return create_hash_from_entry(self.model_dump(exclude={'hash'}))
