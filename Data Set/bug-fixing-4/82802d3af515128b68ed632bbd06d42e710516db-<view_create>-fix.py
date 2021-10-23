def view_create(self, request, group, **kwargs):
    auth_errors = self.check_config_and_auth(request, group)
    if auth_errors:
        return Response(auth_errors, status=400)
    event = group.get_latest_event()
    if (event is None):
        return Response({
            'message': 'Unable to create issues: there are no events associated with this group',
        }, status=400)
    Event.objects.bind_nodes([event], 'data')
    try:
        fields = self.get_new_issue_fields(request, group, event, **kwargs)
    except Exception as e:
        return self.handle_api_error(e)
    if (request.method == 'GET'):
        return Response(fields)
    errors = self.validate_form(fields, request.DATA)
    if errors:
        return Response({
            'error_type': 'validation',
            'errors': errors,
        }, status=400)
    try:
        issue = self.create_issue(group=group, form_data=request.DATA, request=request)
    except Exception as e:
        return self.handle_api_error(e)
    if (not isinstance(issue, dict)):
        issue = {
            'id': issue,
        }
    issue_field_map = self.get_issue_field_map()
    for (key, meta_name) in six.iteritems(issue_field_map):
        if (key in issue):
            GroupMeta.objects.set_value(group, meta_name, issue[key])
        else:
            GroupMeta.objects.unset_value(group, meta_name)
    issue_information = {
        'title': (issue.get('title') or request.DATA.get('title') or self._get_issue_label_compat(group, issue)),
        'provider': self.get_title(),
        'location': self._get_issue_url_compat(group, issue),
        'label': self._get_issue_label_compat(group, issue),
    }
    Activity.objects.create(project=group.project, group=group, type=Activity.CREATE_ISSUE, user=request.user, data=issue_information)
    issue_tracker_used.send(plugin=self, project=group.project, user=request.user, sender=type(self))
    return Response({
        'issue_url': self.get_issue_url(group, issue),
    })