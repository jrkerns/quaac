import json
import zlib


def create_hash_from_entry(entry: dict) -> int:
    """Create an MD5 hash of the given content. This is for creating keys for the files, equipment and data points on the fly."""
    entry_str = json.dumps(entry, sort_keys=True).encode('utf-8')
    return zlib.crc32(entry_str)


def check_hash_from_entry(entry: dict) -> None:
    """Check that the hash matches the entry"""
    # first, pop the hash
    hash = entry.pop('hash')
    # check the hash against the rest of the entry
    if not hash == create_hash_from_entry(entry):
        raise ValueError(f"Hash {hash} does not match its entry.")

