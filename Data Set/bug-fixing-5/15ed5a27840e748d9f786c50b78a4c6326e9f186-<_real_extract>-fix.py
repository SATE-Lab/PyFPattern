def _real_extract(self, url):
    page_id = self._match_id(url)
    webpage = self._download_webpage(url, page_id)
    entries = []
    for player_element in re.findall('(<[^>]+class="kalturaPlayer[^"]*"[^>]*>)', webpage):
        player_params = extract_attributes(player_element)
        if (player_params.get('data-type') not in ('kaltura_singleArticle',)):
            self.report_warning('Unsupported player type')
            continue
        entry_id = player_params['data-id']
        entries.append(self.url_result(('kaltura:1750922:' + entry_id), 'Kaltura', entry_id))
    return self.playlist_result(entries, page_id)