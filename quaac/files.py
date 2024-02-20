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


# def parse_file_entry(document: File) -> bytes:
#     """Parse a QuAACS document spec.
#
#     We decode according to the encoding key and possibly decompress according to the compression key.
#     We then use the MIME type to load the content into the appropriate Python object."""
#     # Get the decoder and decompresser
#     decoder = get_decoder(document['encoding'])
#     decompresser = get_decompresser(document['compression'])
#     # Decode and decompress the content
#     content = decoder(document['content'])
#     content = decompresser(content)
#     return content
