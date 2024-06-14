from __future__ import annotations

import hashlib
import json

from functools import cached_property
from typing import Any

from pydantic import BaseModel, Field, computed_field, model_validator
from pydantic_core.core_schema import ValidationInfo


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


def create_hash_from_entry(entry: dict) -> str:
    """Create an MD5 hash of the given content. This is for creating keys for the files, equipment and data points on the fly."""
    entry_str = json.dumps(entry, sort_keys=True).encode('utf-8')
    return hashlib.md5(entry_str).hexdigest()


def split_hash(named_hash: str) -> str:
    """Split a hash into its type and hash value."""
    return named_hash.split(')')[-1].strip()
