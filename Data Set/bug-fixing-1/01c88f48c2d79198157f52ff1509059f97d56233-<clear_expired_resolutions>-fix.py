

@instrumented_task(name='sentry.tasks.clear_expired_resolutions', time_limit=15, soft_time_limit=10)
def clear_expired_resolutions(release_id):
    '\n    This should be fired when ``release_id`` is created, and will indicate to\n    the system that any pending resolutions older than the given release can now\n    be safely transitioned to resolved.\n    '
    try:
        release = Release.objects.get_from_cache(id=release_id)
    except Release.DoesNotExist:
        return
    resolution_list = list(GroupResolution.objects.filter(release__projects=release.projects.all(), release__date_added__lt=release.date_added).exclude(release=release))
    if (not resolution_list):
        return
    GroupResolution.objects.filter(id__in=[r.id for r in resolution_list]).update(status=GroupResolutionStatus.RESOLVED)
    for resolution in resolution_list:
        try:
            activity = Activity.objects.filter(group=resolution.group_id, type=Activity.SET_RESOLVED_IN_RELEASE, ident=resolution.id).order_by('-datetime')[0]
        except IndexError:
            continue
        activity.update(data={
            'version': release.version,
        })
