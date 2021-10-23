

@instrumented_task(name='sentry.tasks.collect_project_platforms', queue='stats')
def collect_project_platforms(**kwargs):
    now = timezone.now()
    min_project_id = 0
    max_project_id = (Project.objects.aggregate(x=Max('id'))['x'] or 0)
    step = 1000
    while (min_project_id <= max_project_id):
        queryset = Group.objects.filter(last_seen__gte=(now - timedelta(days=1)), project__gte=min_project_id, project__lt=(min_project_id + step), platform__isnull=False).values_list('platform', 'project_id').distinct()
        for (platform, project_id) in queryset:
            platform = platform.lower()
            if (platform not in VALID_PLATFORMS):
                continue
            ProjectPlatform.objects.create_or_update(project_id=project_id, platform=platform, values={
                'last_seen': now,
            })
        min_project_id += step
    ProjectPlatform.objects.filter(last_seen__lte=(now - timedelta(days=90))).delete()
