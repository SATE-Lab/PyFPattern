def check(self):
    if settings.CELERY_ALWAYS_EAGER:
        return []
    last_ping = (options.get('sentry:last_worker_ping') or 0)
    if (last_ping >= (time() - 300)):
        return []
    (backlogged, size) = (None, 0)
    from sentry.monitoring.queues import backend
    if (backend is not None):
        size = backend.get_size('default')
        backlogged = (size > 0)
    message = "Background workers haven't checked in recently. "
    if backlogged:
        message += ("It seems that you have a backlog of %d tasks. Either your workers aren't running or you need more capacity." % size)
    else:
        message += "This is likely an issue with your configuration or the workers aren't running."
    return [Problem(message, url=absolute_uri(reverse('sentry-admin-queue')))]