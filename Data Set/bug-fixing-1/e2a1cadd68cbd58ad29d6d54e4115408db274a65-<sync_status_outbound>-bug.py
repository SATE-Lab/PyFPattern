

@instrumented_task(name='sentry.tasks.integrations.sync_status_outbound', queue='integrations', default_retry_delay=(60 * 5), max_retries=5)
@retry(exclude=(ExternalIssue.DoesNotExist, Integration.DoesNotExist))
def sync_status_outbound(group_id, external_issue_id, **kwargs):
    try:
        group = Group.objects.filter(id=group_id, status__in=[GroupStatus.UNRESOLVED, GroupStatus.RESOLVED])[0]
    except IndexError:
        return
    has_issue_sync = features.has('organizations:integrations-issue-sync', group.organization)
    if (not has_issue_sync):
        return
    external_issue = ExternalIssue.objects.get(id=external_issue_id)
    integration = Integration.objects.get(id=external_issue.integration_id)
    installation = integration.get_installation(organization_id=external_issue.organization_id)
    if installation.should_sync('outbound_status'):
        installation.sync_status_outbound(external_issue, (group.status == GroupStatus.RESOLVED), group.project_id)
        analytics.record('integration.issue.status.synced', provider=integration.provider, id=integration.id, organization_id=external_issue.organization_id)
