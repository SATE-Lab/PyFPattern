

def get_tag_value_paginator_for_projects(self, projects, environments, key, start, end, query=None, order_by='-last_seen'):
    "\n        Includes tags and also snuba columns, with the arrayjoin when they are nested.\n        Also supports a query parameter to do a substring match on the tag/column values.\n        >>> get_tag_value_paginator_for_projects([1], [2], 'environment', query='prod')\n        "
    raise NotImplementedError
