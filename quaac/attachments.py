import base64
import gzip


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
