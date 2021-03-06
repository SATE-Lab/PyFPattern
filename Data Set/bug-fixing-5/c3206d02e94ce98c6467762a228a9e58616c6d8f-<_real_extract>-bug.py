def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    if ('The content you are trying to access is not available in your region.' in webpage):
        self.raise_geo_restricted()
    video_data = extract_attributes(self._search_regex('(<a.+?rel="http://link\\.theplatform\\.com/s/.+?</a>)', webpage, 'video data'))
    player_type = self._search_regex('playerType\\s*=\\s*[\\\'"]([^\\\'"]+)', webpage, 'player type', default=None)
    release_url = video_data['rel']
    title = video_data['data-title']
    rating = video_data.get('data-rating')
    query = {
        'mbr': 'true',
    }
    if (player_type == 'movies'):
        query.update({
            'manifest': 'm3u',
        })
    else:
        query.update({
            'switch': 'http',
        })
    if (video_data.get('data-req-auth') == '1'):
        resource = self._get_mvpd_resource(video_data['data-channel'], title, video_data.get('data-guid'), rating)
        query['auth'] = self._extract_mvpd_auth(url, video_id, 'fx', resource)
    return {
        '_type': 'url_transparent',
        'id': video_id,
        'title': title,
        'url': smuggle_url(update_url_query(release_url, query), {
            'force_smil_url': True,
        }),
        'thumbnail': video_data.get('data-large-thumb'),
        'age_limit': parse_age_limit(rating),
        'ie_key': 'ThePlatform',
    }