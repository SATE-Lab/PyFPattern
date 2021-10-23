def bulk_fetch_project_latest_releases(projects):
    "\n    Fetches the latest release for each of the passed projects\n    :param projects:\n    :return: List of Releases, each with an additional `actual_project_id`\n    attribute representing the project that they're the latest release for. If\n    no release found, no entry will be returned for the given project.\n    "
    return list(Release.objects.raw('\n        SELECT lr.project_id as actual_project_id, r.*\n        FROM (\n            SELECT (\n                SELECT lrr.id\n                FROM sentry_release lrr\n                JOIN sentry_release_project lrp ON lrp.release_id = lrr.id\n                WHERE lrp.project_id = p.id\n                ORDER BY COALESCE(lrr.date_released, lrr.date_added) DESC\n                LIMIT 1\n            ) as release_id,\n            p.id as project_id\n            FROM sentry_project p\n            WHERE p.id IN ({})\n        ) as lr\n        JOIN sentry_release r\n        ON r.id = lr.release_id\n        '.format(', '.join((six.text_type(i.id) for i in projects)))))