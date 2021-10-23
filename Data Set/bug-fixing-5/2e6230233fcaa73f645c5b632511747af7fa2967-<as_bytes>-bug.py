def as_bytes(bytes_or_text, encoding='utf-8'):
    'Converts either `bytes` or unicode python input types to `bytes`.\n\n  Uses utf-8 encoding for text by default.\n\n  Args:\n    bytes_or_text: A `bytes`, `str`, or `unicode` object.\n    encoding: A string indicating the charset for encoding unicode.\n\n  Returns:\n    A `bytes` object.\n\n  Raises:\n    TypeError: If `bytes_or_text` is not a binary or unicode string.\n  '
    if isinstance(bytes_or_text, _six.text_type):
        return bytes_or_text.encode(encoding)
    elif isinstance(bytes_or_text, bytes):
        return bytes_or_text
    else:
        raise TypeError(('Expected binary or unicode string, got %r' % (bytes_or_text,)))