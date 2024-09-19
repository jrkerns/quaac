from __future__ import annotations

import base64
import gzip
from pathlib import Path

from pydantic import ConfigDict, Field

from .common import HashModel
from . import peewee_models as pw


class Compression:
    """Compression algorithms supported by QuAACS.

    GZIP: Gzip compression.
    NONE: No compression.
    """

    GZIP = {'compression': 'gzip', 'compress': gzip.compress, 'decompress': gzip.decompress}
    NONE = {'compression': None, 'compress': lambda x: x, 'decompress': lambda x: x}


class Encoding:
    """Encoding algorithms supported by QuAACS.

    BASE64: Base64 encoding.
    """

    BASE64 = {'encoding': 'base64', 'encoder': base64.b64encode, 'decoder': base64.b64decode}


def get_decoder(encoding: str):
    """Get the encoder function for the given encoding."""
    if encoding == Encoding.BASE64['encoding']:
        return Encoding.BASE64['decoder']
    else:
        raise ValueError(f"Unsupported encoding: {encoding}")


def get_compressor(compression: str | None):
    """Get the compression function for the given compression."""
    if compression == Compression.GZIP['compression']:
        return Compression.GZIP['compress']
    elif compression is None:
        return Compression.NONE['compress']
    else:
        raise ValueError(f"Unsupported compression: {compression}")


def get_decompresser(compression: str):
    """Get the compression function for the given compression."""
    if compression == Compression.GZIP['compression']:
        return Compression.GZIP['decompress']
    elif compression is None:
        return Compression.NONE['decompress']
    else:
        raise ValueError(f"Unsupported compression: {compression}")


def get_encoder(encoding: str) -> callable:
    """Get the encoder function for the given encoding."""
    if encoding == Encoding.BASE64['encoding']:
        return Encoding.BASE64['encoder']
    else:
        raise ValueError(f"Unsupported encoding: {encoding}")


class Attachment(HashModel, pw.PeeWeeMixin, validate_assignment=True):
    """A binary file that relates to a data point. This could be a screenshot, DICOM data set, or a PDF."""
    model_config = ConfigDict(title="Attachment", frozen=True, str_strip_whitespace=True, extra='allow', populate_by_name=True)
    name: str = Field(title="Name", description="The name of the file.", examples=["catphan.zip", "screenshot.png"])
    comment: str = Field(default="", title="Comment", description="A comment about the file.", examples=["This is the screenshot of the CBCT"])
    encoding: str = Field(title="Encoding", default='base64', description="The encoding of the file.", examples=["base64"])
    compression: str | None = Field(title="Compression", default='gzip', description="The compression of the file.", examples=["gzip"])
    # we don't use a pydantic encoder here because we use the other field values to determine the encoding and compression
    # that isn't possible within a pydantic encoder
    content: bytes = Field(title="Content", description="The content of the file.", examples=["b'H4sIAAAAAAAAA...'"])

    def _to_peewee(self, db_path: Path) -> int:
        """Save the attachment to the database and store the file
        itself beside the database file."""
        storage_dir = db_path.parent.absolute() / db_path.with_name('attachments')
        storage_dir.mkdir(exist_ok=True)
        f_path = self.to_file(path=storage_dir / self.hash)
        rel_path = f_path.relative_to(db_path.parent.absolute())
        return pw.Attachment.get_or_create(name=self.name, comment=self.comment, encoding=self.encoding, compression=self.compression, file_name=rel_path)[0]

    def to_file(self, path: Path | str | None = None) -> Path:
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
        path = Path(path or self.name).absolute()
        if path.is_dir():
            path = path / self.name
        with open(path, 'wb') as f:
            f.write(decomp_content)
        return path

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

            .. note:: This is not saying that the file is ALREADY compressed. This is the compression that **will** be applied when serializing the file.

        encoding : str
            The encoding to use when serializing the file. Default is 'base64'.

            .. note:: This is not saying that the file is ALREADY encoded. This is the encoding that **will** be applied when serializing the file.
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
