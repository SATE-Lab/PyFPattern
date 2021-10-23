

def _extract_series(self, webpage, display_id, fatal=True):
    config = self._parse_json(self._search_regex(('INITIAL_DATA_*\\s*=\\s*({.+?})\\s*;', '({.+?})\\s*,\\s*"[^"]+"\\s*\\)\\s*</script>'), webpage, 'config', default=('{}' if (not fatal) else NO_DEFAULT)), display_id, fatal=False)
    if (not config):
        return
    return try_get(config, ((lambda x: x['initialState']['series']), (lambda x: x['series'])), dict)
