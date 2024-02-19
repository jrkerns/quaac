import base64
import gzip
import mimetypes
from dataclasses import dataclass, field, asdict
from pathlib import Path

from quaacs.hashers import create_hash_from_entry


@dataclass
class File:
    """A file defined in a YAML spec file."""
    name: str
    type: str
    encoding: str
    compression: str
    content: str
    hash: int = field(init=False, default=None)

    def __post_init__(self):
        self.hash = create_hash_from_entry(asdict(self))


class Compression:
    """Compression algorithms supported by QuAACS."""

    GZIP = {'compression': 'gzip', 'compress': gzip.compress, 'decompress': gzip.decompress}
    NONE = {'compression': None, 'compress': lambda x: x, 'decompress': lambda x: x}


class Encoding:
    """Encoding algorithms supported by QuAACS."""

    BASE64 = {'encoding': 'base64', 'encoder': base64.b64encode, 'decoder': base64.b64decode}


def get_decoder(encoding: str):
    """Get the encoder function for the given encoding."""
    if encoding == Encoding.BASE64['encoding']:
        return Encoding.BASE64['decoder']
    else:
        raise ValueError(f"Unsupported encoding: {encoding}")


def get_compressor(compression: str):
    """Get the compression function for the given compression."""
    if compression == Compression.GZIP['compression']:
        return Compression.GZIP['compress']
    else:
        raise ValueError(f"Unsupported compression: {compression}")


def get_decompresser(compression: str):
    """Get the compression function for the given compression."""
    if compression == Compression.GZIP['compression']:
        return Compression.GZIP['decompress']
    else:
        raise ValueError(f"Unsupported compression: {compression}")


def get_encoder(encoding: str) -> callable:
    """Get the encoder function for the given encoding."""
    if encoding == Encoding.BASE64['encoding']:
        return Encoding.BASE64['encoder']
    else:
        raise ValueError(f"Unsupported encoding: {encoding}")


def create_file_entry(path: Path, encoding: str = 'base64', compression: str | None = 'gzip') -> File:
    """Create a file entry for a given file from disk.

    Parameters
    ----------
    path : Path
        The path to the file.
    encoding : str, optional
        The encoding to use. Default is base64.
    compression : str, optional
        The compression to use. Default is gzip.
    """
    with open(path, 'rb') as file:
        content = file.read()
    if compression:
        compressor = get_compressor(compression)
        content = compressor(content)
    # encode
    encoder = get_encoder(encoding)
    content = encoder(content).decode('utf-8')
    entry = File(
        name=path.name,
        type=mimetypes.guess_type(path)[0],
        encoding=encoding,
        compression=compression,
        content=content,
    )
    return entry


def parse_file_entry(document: File) -> bytes:
    """Parse a QuAACS document spec.

    We decode according to the encoding key and possibly decompress according to the compression key.
    We then use the MIME type to load the content into the appropriate Python object."""
    # Get the decoder and decompresser
    decoder = get_decoder(document['encoding'])
    decompresser = get_decompresser(document['compression'])
    # Decode and decompress the content
    content = decoder(document['content'])
    content = decompresser(content)
    return content
