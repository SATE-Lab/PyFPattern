def handle(self, request, organization, project, client_event_id):
    '\n        Given a client event id and project, redirects to the event page\n        '
    use_snuba = options.get('snuba.events-queries.enabled')
    event_cls = (SnubaEvent if use_snuba else Event)
    event = event_cls.objects.from_event_id(client_event_id, project.id)
    if (event is None):
        raise Http404
    if features.has('organizations:sentry10', organization, actor=request.user):
        return HttpResponseRedirect(reverse('sentry-organization-event-detail', args=[organization.slug, event.group_id, event.id]))
    return HttpResponseRedirect(reverse('sentry-group-event', args=[organization.slug, event.project.slug, event.group_id, event.id]))