

@attach_scenarios([create_hook_scenario])
def post(self, request, project):
    '\n        Register a new Service Hook\n        ```````````````````````````\n\n        Register a new service hook on a project.\n\n        Events include:\n\n        - event.alert: An alert is generated for an event (via rules).\n        - event.created: A new event has been processed.\n\n        :pparam string organization_slug: the slug of the organization the\n                                          client keys belong to.\n        :pparam string project_slug: the slug of the project the client keys\n                                     belong to.\n        :param string url: the url for the webhook\n        :param array[string] events: the events to subscribe to\n        '
    if (not request.user.is_authenticated()):
        return self.respond(status=401)
    validator = ServiceHookValidator(data=request.DATA)
    if (not validator.is_valid()):
        return self.respond(validator.errors, status=status.HTTP_400_BAD_REQUEST)
    result = validator.object
    with transaction.atomic():
        hook = ServiceHook.objects.create(project_id=project.id, url=result['url'], actor_id=request.user.id, events=result.get('events'), application=(getattr(request.auth, 'application', None) if request.auth else None))
        self.create_audit_entry(request=request, organization=project.organization, target_object=hook.id, event=AuditLogEntryEvent.SERVICEHOOK_ADD, data=hook.get_audit_log_data())
    return self.respond(serialize(hook, request.user), status=201)
