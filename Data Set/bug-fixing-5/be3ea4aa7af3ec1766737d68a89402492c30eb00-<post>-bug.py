def post(self, request, group):
    serializer = NoteSerializer(data=request.DATA, context={
        'group': group,
    })
    if (not serializer.is_valid()):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    data = dict(serializer.object)
    mentions = data.pop('mentions', [])
    if Activity.objects.filter(group=group, type=Activity.NOTE, user=request.user, data=data, datetime__gte=(timezone.now() - timedelta(hours=1))).exists():
        return Response('{"detail": "You have already posted that comment."}', status=status.HTTP_400_BAD_REQUEST)
    GroupSubscription.objects.subscribe(group=group, user=request.user, reason=GroupSubscriptionReason.comment)
    actors = Actor.resolve_many(mentions)
    actor_mentions = seperate_resolved_actors(actors)
    for user in actor_mentions.get('users'):
        GroupSubscription.objects.subscribe(group=group, user=user, reason=GroupSubscriptionReason.mentioned)
    mentioned_teams = actor_mentions.get('teams')
    mentioned_team_users = list(User.objects.filter(sentry_orgmember_set__organization_id=group.project.organization_id, sentry_orgmember_set__organizationmemberteam__team__in=mentioned_teams, sentry_orgmember_set__organizationmemberteam__is_active=True, is_active=True).exclude(id__in={u.id for u in actor_mentions.get('users')}).values_list('id', flat=True))
    GroupSubscription.objects.bulk_subscribe(group=group, user_ids=mentioned_team_users, reason=GroupSubscriptionReason.team_mentioned)
    activity = Activity.objects.create(group=group, project=group.project, type=Activity.NOTE, user=extract_lazy_object(request.user), data=data)
    activity.send_notification()
    if features.has('organizations:internal-catchall', group.organization, actor=request.user):
        external_issue_ids = GroupLink.objects.filter(project_id=group.project_id, group_id=group.id, linked_type=GroupLink.LinkedType.issue).values_list('linked_id', flat=True)
        for external_issue_id in external_issue_ids:
            post_comment.apply_async(kwargs={
                'external_issue_id': external_issue_id,
                'data': data,
            })
    return Response(serialize(activity, request.user), status=201)