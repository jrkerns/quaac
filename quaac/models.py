from __future__ import annotations

import hashlib
import json
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, computed_field, Field, field_serializer, ConfigDict, model_validator, EmailStr
from pydantic_core.core_schema import ValidationInfo

from .attachments import get_decoder, get_decompresser, get_encoder, get_compressor


def create_hash_from_entry(entry: dict) -> str:
    """Create an MD5 hash of the given content. This is for creating keys for the files, equipment and data points on the fly."""
    entry_str = json.dumps(entry, sort_keys=True).encode('utf-8')
    return hashlib.md5(entry_str).hexdigest()


def split_hash(named_hash: str) -> str:
    """Split a hash into its type and hash value."""
    return named_hash.split(')')[-1].strip()


class HashModel(BaseModel):
    """A mixin to add a computed hash field to a model. This also checks the hash
    on the way in from a file to ensure it hasn't changed.

     This verifies that data has not been modified since it was created."""
    from_file_hash: str | None = Field(exclude=True, default=None, description="The original hash of the entry. Only populates when loading from JSON/YAML.")

    @computed_field()
    @cached_property
    def hash(self) -> str:
        """A dynamic MD5 hash of the entry. This is used to create keys for the files, equipment and data points on the fly."""
        return create_hash_from_entry(self.model_dump(exclude={'hash'}, mode='json'))

    @model_validator(mode='before')
    @classmethod
    def save_original_hash_key(cls: dict, data: Any, info: ValidationInfo) -> dict:
        """Check that the hash key from the file matches the dynamic hash. This only happens when loading from JSON/YAML."""
        # this is None when creating the model.
        original_hash = data.pop('hash', None)
        if info.context and info.context.get('check_hash', True):
            data['from_file_hash'] = original_hash
        return data

    @model_validator(mode='after')
    def check_hash(self):
        """Check that the hash key from the file matches the dynamic hash. This only happens when loading from JSON/YAML."""
        if self.from_file_hash and self.hash != self.from_file_hash:
            raise ValueError("The hash key from the file does not match the dynamic hash. The file has been edited since created.")
        return self

    def named_hash(self) -> str:
        """Return the hash with the name of the object. Adds some clarity when perusing a QuAAC document."""
        return f"({self.name}) {self.hash}"


class DataPoint(HashModel, validate_assignment=True):
    """A singular measurement of a quality assurance session."""
    model_config = ConfigDict(title="DataPoint", description="A data point defined in a YAML spec file.", ser_json_bytes='utf8', ser_json_timedelta='iso8601', str_strip_whitespace=True, extra='allow', populate_by_name=True)

    name: str = Field(title="Name", description="The name of the datapoint.", examples=["Temperature", "6MV Output", 'CBCT Spotlight Uniformity Center'])
    perform_datetime: datetime = Field(title="Perform Datetime", alias="perform datetime", description="The date and time the measurement was performed. Must be in ISO 8601 format.", examples=["2021-08-01T12:00:00"])
    measurement_value: Any = Field(title="Measurement Value", alias="measurement value", description="The value of the measurement.", examples=[1, 1.0, "1", "1.0"])
    measurement_unit: str = Field(title="Measurement Unit", alias="measurement unit", description="The unit of the measurement.", examples=["cGy", "Celsius", "mm", "nC", "cm"])
    reference_value: Any | None = Field(default=None, alias="reference value", title="Reference Value", description="The reference value of the measurement.", examples=[1, 1.0, "1", "1.0"])
    description: str = Field(default="", title="Description", description="A description of the measurement. This can reference any specific equations or algorithms used.", examples=["Based on TG-51 eqn 8"])
    procedure: str = Field(default="", title="Procedure", description="The instructions used to perform the measurement.", examples=["Use blocks A and D on the couch with 10x10cm field size. SSD=100 to top of block A"])
    performer: User = Field(title="Performer", description="The user who performed the measurement.", examples=["1"], json_schema_extra={'type': 'string'})
    performer_comment: str = Field(default="", alias="performer comment", title="Performer Comment", description="Any comments the performer has about the measurement.", examples=["The temperature was 22C"])
    primary_equipment: Equipment = Field(title="Primary Equipment", alias="primary equipment", description="The equipment used to perform the measurement.", examples=["1"], json_schema_extra={'type': 'string'})
    reviewer: User | None = Field(default=None, title="Reviewer", description="The user who reviewed the data point.", examples=["1"], json_schema_extra={'type': 'string'})
    parameters: dict[str, Any] = Field(default_factory=dict, title="Parameters", description="Any parameters used to perform the measurement.", examples=[{"field_size": "10x10cm", "ssd": "100cm"}])
    ancillary_equipment: list[Equipment] = Field(default_factory=list, alias="ancillary equipment", title="Ancillary Equipment", description="The internal IDs of any ancillary equipment used to perform the measurement.", examples=["1"], json_schema_extra={'type': 'string'})
    attachments: list[Attachment] = Field(default_factory=list, title="Attachments", description="The files associated with the measurement.", examples=["1"], json_schema_extra={'type': 'string'})

    @field_serializer('primary_equipment', when_used='json')
    def serialize_primary_equipment(self, primary_equipment: Equipment, _info) -> str:
        """Serialize the primary equipment to its hash. This happens when dumped to JSON/YAML so
        that only the hash is serialized. When saving a document, a separate section is created for the equipment."""
        return f"({primary_equipment.name}) {primary_equipment.hash}"

    @field_serializer('ancillary_equipment', when_used='json')
    def serialize_ancillary_equipment(self, ancillary_equipment: list[Equipment], _info) -> list[str]:
        """Serialize the ancillary equipment to their hashes. This happens when dumped to JSON/YAML just as for primary equipment"""
        return [f"({e.name}) {e.hash}" for e in ancillary_equipment]

    @field_serializer('performer', when_used='json')
    def serialize_performer(self, performer: User, _info) -> str:
        """Serialize the performer to their hash. This happens when dumped to JSON/YAML just as for primary equipment"""
        return f"({performer.name}) {performer.hash}"

    @field_serializer('reviewer', when_used='json-unless-none')
    def serialize_reviewer(self, reviewer: User, _info) -> str:
        """Serialize the reviewer to their hash. This happens when dumped to JSON/YAML just as for primary equipment"""
        return f"({reviewer.name}) {reviewer.hash}"

    @field_serializer('attachments', when_used='json')
    def serialize_attachments(self, attachments: list[Attachment], _info) -> list[str]:
        """Serialize the attachments to their hashes. This happens when dumped to JSON/YAML just as for primary equipment"""
        return [f"({f.name}) {f.hash}" for f in attachments]


class Equipment(HashModel, validate_assignment=True):
    """A peice of equipment. This could be primary equipment such as a linac or ancillary equipment such as a phantom or chamber."""
    model_config = ConfigDict(title="Equipment", frozen=True, str_strip_whitespace=True, extra='allow', populate_by_name=True)
    name: str = Field(title="Name", description="The name of the equipment.", examples=["TrueBeam 1", "Basement 600"])
    type: str = Field(title="Type", description="The type of the equipment.", examples=["L", "CT scanner"])
    serial_number: str = Field(title="Serial Number", alias="serial number", description="The serial number of the equipment.", examples=["12345", "H192311"])
    manufacturer: str = Field(title="Manufacturer", description="The manufacturer of the equipment.", examples=["Varian", "Siemens"])
    model: str = Field(title="Model", description="The model of the equipment.", examples=["TrueBeam", "Artiste"])


class User(HashModel, validate_assignment=True):
    """A user. This could be the performer or reviewer of a data point."""
    model_config = ConfigDict(title="User", frozen=True, str_strip_whitespace=True, extra='allow', populate_by_name=True)
    name: str = Field(title="Name", description="The name of the user.", examples=["John Doe", "Jane Smith"])
    email: EmailStr = Field(title="Email", description="The email of the user.", examples=["john@clinic.com", "jane@satellite.com"])


class Attachment(HashModel, validate_assignment=True):
    """A binary file that relates to a data point. This could be a screenshot, DICOM data set, or a PDF."""
    model_config = ConfigDict(title="Attachment", frozen=True, str_strip_whitespace=True, extra='allow', populate_by_name=True)
    name: str = Field(title="Name", description="The name of the file.", examples=["catphan.zip", "screenshot.png"])
    comment: str = Field(default="", title="Comment", description="A comment about the file.", examples=["This is the screenshot of the CBCT"])
    encoding: str = Field(title="Encoding", default='base64', description="The encoding of the file.", examples=["base64"])
    compression: str | None = Field(title="Compression", default='gzip', description="The compression of the file.", examples=["gzip"])
    # we don't use a pydantic encoder here because we use the other field values to determine the encoding and compression
    # that isn't possible within a pydantic encoder
    content: bytes = Field(title="Content", description="The content of the file.", examples=["b'H4sIAAAAAAAAA...'"])

    def to_file(self, path: str | None = None) -> None:
        """Write the content of an attachment to a file on disk.

        Parameters
        ----------
        path : str, optional
            The path to write the file to. If None, the name of the file in the document will be used and
            will be written to the current working directory.
        """
        decoder = get_decoder(self.encoding)
        decompressor = get_decompresser(self.compression)
        # Decode and decompress the content
        decoded_content = decoder(self.content)
        decomp_content = decompressor(decoded_content)
        path = path or self.name
        with open(path, 'wb') as f:
            f.write(decomp_content)

    @classmethod
    def from_file(cls, path: str | Path, name: str | None = None, type: str | None = None, comment: str = '', compression: str | None = 'gzip', encoding: str = 'base64') -> Attachment:
        """Load a file from disk into an attachment.

        Parameters
        ----------
        path : str or Path
            The path to the file to load.
        name: str | None
            The name of the file. If None, the name of the passed file will be used.
        type : str | None
            The type of the file. E.g. png, json, zip, etc. If None, the extension of the file will be used.
            The type is not enforced and is not used for anything other than display.
        comment : str
            A comment about the file.
        compression : str | None
            The compression to use when serializing the file. Default is 'gzip'.
            If None, no compression will be used.

            .. note:: This is not the saying that the file is ALREADY compressed. This is the compression that **will** be applied only when serializing the file.

        encoding : str
            The encoding to use when serializing the file. Default is 'base64'.

            .. note:: This is not the saying that the file is ALREADY encoded. This is the encoding that **will** be applied only when serializing the file.
        """
        path = Path(path)  # force-convert to Path
        with open(path, 'rb') as f:
            raw_content = f.read()
        encoder = get_encoder(encoding)
        compressor = get_compressor(compression)
        # Decode and decompress the content
        comp_content = compressor(raw_content)
        enc_content = encoder(comp_content)
        return Attachment(name=name or path.name, type=type or path.suffix.replace('.', ''), encoding=encoding, comment=comment, compression=compression, content=enc_content)


class Document(HashModel, validate_assignment=True):
    """The top-level model for QuAAC. Contains data points."""
    model_config = ConfigDict(title="Document", str_strip_whitespace=True, populate_by_name=True, extra='allow')
    version: Literal['1.0'] = Field(title="Version", default="1.0", description="The version of the QuAAC document.")
    datapoints: list[DataPoint] = Field(title="Data Points", description="The data points in the document.")

    @computed_field(return_type=set[Equipment])
    @property
    def equipment(self) -> set[Equipment]:
        """The unique equipment from the datapoints."""
        return {d.primary_equipment for d in self.datapoints} | {e for d in self.datapoints for e in
                                                                 d.ancillary_equipment}

    @computed_field(return_type=set[User])
    @property
    def users(self) -> set[User]:
        """The unique users from the datapoints."""
        return {d.performer for d in self.datapoints} | {d.reviewer for d in self.datapoints if d.reviewer is not None}

    @computed_field(return_type=set[Attachment])
    @property
    def attachments(self) -> set[Attachment]:
        """The unique attachments from the datapoints."""
        return {f for d in self.datapoints for f in d.attachments}

    def to_json_file(self, path: str, indent: int = 4) -> None:
        """Write the document to a JSON file."""
        with open(path, 'w') as f:
            f.write(self.model_dump_json(indent=indent, by_alias=True))

    @classmethod
    def from_json_file(cls, path: str, check_hash: bool = True) -> Document:
        """Load a document from a JSON file.

        Parameters
        ----------
        path : str
            The path to the JSON file.
        check_hash : bool
            Whether to check the hash of the file. This is True by default. If the file has been edited since it was created, an error will be raised.
        """
        with open(path, 'r') as f:
            return Document.model_validate_json(f.read(), context={'check_hash': check_hash})

    def to_yaml_file(self, path: str) -> None:
        """Write the document to a YAML file."""
        doc_yaml = yaml.safe_load(self.model_dump_json(by_alias=True))
        with open(path, 'w') as f:
            yaml.dump(doc_yaml, f, sort_keys=False)

    @classmethod
    def from_yaml_file(cls, path: str, check_hash: bool = True) -> Document:
        """Load a document from a YAML file."""
        with open(path, 'r') as f:
            json_str = json.dumps(yaml.safe_load(f))
            return Document.model_validate_json(json_str)

    def merge(self, documents: list[Document]) -> Document:
        """Merge other documents into a new document."""
        # check versions are the same
        if any(d.version != self.version for d in documents):
            raise ValueError("All documents must have the same version to merge.")

        # get all unique data points
        all_data_points = self.datapoints + [datapoint for doc in documents for datapoint in doc.datapoints]

        return Document(datapoints=all_data_points)

    @model_validator(mode='before')
    @classmethod
    def replace_hash_keys(cls, data: dict, info: ValidationInfo):
        """When loading from JSON/YAML, replace the hashes of equipment, users, and attachments with the actual objects."""
        # in python mode, objects are already loaded
        if info.mode == 'python':
            return data
        # Create a lookup table for each type of object
        equipment = {e['hash']: e for e in data['equipment']}
        users = {u['hash']: u for u in data['users']}
        attachments = {a['hash']: a for a in data['attachments']}
        # Replace the hashes with the actual objects
        for d in data['datapoints']:
            d['primary equipment'] = equipment[split_hash(d['primary equipment'])]
            d['ancillary equipment'] = [equipment[split_hash(a)] for a in d['ancillary equipment']]
            d['performer'] = users[split_hash(d['performer'])]
            if d['reviewer']:
                d['reviewer'] = users[split_hash(d['reviewer'])]
            d['attachments'] = [attachments[split_hash(f)] for f in d['attachments']]
        return data
