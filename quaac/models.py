from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, computed_field, Field, field_serializer, ConfigDict, model_validator

from quaac.hashers import create_hash_from_entry

class HashMixin:

    @computed_field
    def hash(self) -> str:
        return create_hash_from_entry(self.model_dump(exclude={'hash'}, mode='json'))

    @model_validator(mode='after')
    def check_hash(self):
        hash = create_hash_from_entry(self.model_dump(exclude={'hash'}, mode='json'))
        if not hash == self.hash:
            raise ValueError(f"Hash {self.hash} does not match its entry. This means the entry has been modified since it's creation.")
        return self


class DataPoint(HashMixin, BaseModel, validate_assignment=True):
    """An equipment defined in a YAML spec file."""
    model_config = ConfigDict(title="DataPoint", description="A data point defined in a YAML spec file.", ser_json_bytes='utf8', ser_json_timedelta='iso8601', str_strip_whitespace=True, extra='allow')

    name: str = Field(title="Name", description="The name of the datapoint.", examples=["Temperature", "6MV Output", 'CBCT Spotlight Uniformity Center'])
    perform_datetime: datetime = Field(title="Perform Datetime", description="The date and time the measurement was performed. Must be in ISO 8601 format.", examples=["2021-08-01T12:00:00"])
    measurement_value: Any = Field(title="Measurement Value", description="The value of the measurement.", examples=[1, 1.0, "1", "1.0"])
    measurement_unit: str = Field(title="Measurement Unit", description="The unit of the measurement.", examples=["cGy", "Celsius", "mm", "nC", "cm"])
    reference_value: Any | None = None
    description: str = Field(default="", title="Description", description="A description of the measurement. This can reference any specific equations or algorithms used.", examples=["Based on TG-51 eqn 8"])
    procedure: str = Field(default="", title="Procedure", description="The instructions used to perform the measurement.", examples=["Use blocks A and D on the couch with 10x10cm field size. SSD=100 to top of block A"])
    performer: User = Field(title="Performer", description="The internal ID of the user who performed the measurement.", examples=["1"])
    performer_comment: str = Field(default="", title="Performer Comment", description="Any comments the performer has about the measurement.", examples=["The temperature was 22C"])
    primary_equipment: Equipment = Field(title="Primary Equipment", description="The internal ID of the equipment used to perform the measurement.", examples=["1"])
    reviewer: User | None = Field(default=None, title="Reviewer", description="The internal ID of the user who reviewed the data point.", examples=["1"])
    parameters: dict[str, Any] = Field(default_factory=dict, title="Parameters", description="Any parameters used to perform the measurement.", examples=[{"field_size": "10x10cm", "ssd": "100cm"}])
    ancillary_equipment: list[Equipment] | None = Field(default=None, title="Ancillary Equipment", description="The internal IDs of any ancillary equipment used to perform the measurement.", examples=["1"])
    files: list[Attachment] | None = Field(default=None, title="Files", description="The internal IDs of any files associated with the measurement.", examples=["1"])

    @field_serializer('primary_equipment', when_used='json')
    def serialize_primary_equipment(self, primary_equipment: Equipment, _info) -> str:
        return primary_equipment.hash

    @field_serializer('ancillary_equipment', when_used='json-unless-none')
    def serialize_ancillary_equipment(self, ancillary_equipment: list[Equipment] | None, _info) -> list[str] | None:
        return [e.hash for e in ancillary_equipment]

    @field_serializer('performer', when_used='json')
    def serialize_performer(self, performer: User, _info) -> str:
        return performer.hash

    @field_serializer('reviewer', when_used='json-unless-none')
    def serialize_reviewer(self, reviewer: User | None, _info) -> str | None:
        return reviewer.hash


class Equipment(HashMixin, BaseModel, validate_assignment=True):
    """An equipment defined in a YAML spec file."""
    model_config = ConfigDict(title="Equipment", str_strip_whitespace=True, extra='allow')
    name: str = Field(title="Name", description="The name of the equipment.", examples=["TrueBeam 1", "Basement 600"])
    type: str = Field(title="Type", description="The type of the equipment.", examples=["L", "CT scanner"])
    serial_number: str = Field(title="Serial Number", description="The serial number of the equipment.", examples=["12345", "H192311"])
    manufacturer: str = Field(title="Manufacturer", description="The manufacturer of the equipment.", examples=["Varian", "Siemens"])
    model: str = Field(title="Model", description="The model of the equipment.", examples=["TrueBeam", "Artiste"])


class User(HashMixin, BaseModel, validate_assignment=True):
    """A user defined in a YAML spec file."""
    model_config = ConfigDict(title="User", str_strip_whitespace=True, extra='allow')
    name: str = Field(title="Name", description="The name of the user.", examples=["John Doe", "Jane Smith"])
    email: str = Field(title="Email", description="The email of the user.", examples=["john@clinic.com", "jane@satellite.com"])


class Attachment(HashMixin, BaseModel, validate_assignment=True):
    """A file defined in a YAML spec file."""
    model_config = ConfigDict(title="Attachment", str_strip_whitespace=True, extra='allow')
    name: str = Field(title="Name", description="The name of the file.", examples=["catphan.zip", "screenshot.png"])
    type: str = Field(title="Type", description="The type of the file. Although the filename can have the extension in it, this makes it clear.", examples=["zip", "png"])
    encoding: str = Field(title="Encoding", description="The encoding of the file.", examples=["base64"])
    compression: str = Field(title="Compression", description="The compression of the file.", examples=["gzip"])
    content: str = Field(title="Content", description="The content of the file.", examples=["H4sIAAAAAAAAA..."])


class Document(HashMixin, BaseModel, validate_assignment=True):
    """A document defined in a YAML spec file."""
    model_config = ConfigDict(title="Document", str_strip_whitespace=True, extra='allow')
    version: Literal['1'] = Field(title="Version", description="The version of the QuAAC document.")
    datapoints: list[DataPoint] = Field(title="Data Points", description="The data points in the document.")
    equipment: list[Equipment] = Field(title="Equipment", description="The equipment in the document.")
    users: list[User] = Field(title="Users", description="The users in the document.")
    files: list[Attachment] = Field(title="Files", description="The files in the document.")

