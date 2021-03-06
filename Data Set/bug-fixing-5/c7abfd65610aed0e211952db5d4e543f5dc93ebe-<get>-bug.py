def get(self, request, group):
    has_issue_basic = features.has('organizations:integrations-issue-basic', group.organization, actor=request.user)
    has_issue_sync = features.has('organizations:integrations-issue-sync', group.organization, actor=request.user)
    if ((not has_issue_basic) or has_issue_sync):
        return self.respond([])
    providers = [i.key for i in integrations.all() if (i.has_feature(IntegrationFeatures.ISSUE_BASIC) or i.has_feature(IntegrationFeatures.ISSUE_SYNC))]
    return self.paginate(queryset=Integration.objects.filter(organizations=group.organization, provider__in=providers), request=request, order_by='name', on_results=(lambda x: serialize(x, request.user, IntegrationIssueSerializer(group))), paginator_cls=OffsetPaginator)