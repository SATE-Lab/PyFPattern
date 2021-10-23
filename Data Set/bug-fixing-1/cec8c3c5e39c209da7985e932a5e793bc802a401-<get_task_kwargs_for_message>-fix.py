

def get_task_kwargs_for_message(value):
    '\n    Decodes a message body, returning a dictionary of keyword arguments that\n    can be applied to a post-processing task, or ``None`` if no task should be\n    dispatched.\n    '
    if (len(value) > 10000000):
        logger.debug('Event payload too large: %d', len(value))
        return None
    payload = json.loads(value)
    try:
        version = payload[0]
    except Exception:
        raise InvalidPayload('Received event payload with unexpected structure')
    try:
        handler = version_handlers[int(version)]
    except (ValueError, KeyError):
        raise InvalidVersion('Received event payload with unexpected version identifier: {}'.format(version))
    return handler(*payload[1:])
