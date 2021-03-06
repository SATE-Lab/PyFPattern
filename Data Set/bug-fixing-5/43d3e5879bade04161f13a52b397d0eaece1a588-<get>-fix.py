def get(self, request, organization):
    email = request.GET.get('email')
    if (email is None):
        return Response(status=400)
    limit = request.GET.get('limit', 100)
    project_ids = list(Project.objects.filter(teams__in=OrganizationMemberTeam.objects.filter(organizationmember__user=request.user, organizationmember__organization=organization, is_active=True).values('team')).values_list('id', flat=True)[:1000])
    event_users = list(EventUser.objects.filter(email=email, project_id__in=project_ids)[:1000])
    if event_users:
        groups = Group.objects.filter(id__in=tagstore.get_group_ids_for_users(project_ids=list(set([e.project_id for e in event_users])), event_users=event_users, limit=limit)).order_by('-last_seen')[:limit]
    else:
        groups = []
    context = serialize(list(groups), request.user, GroupSerializer(environment_func=self._get_environment_func(request, organization.id)))
    return Response(context)