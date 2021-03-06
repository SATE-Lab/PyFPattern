def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    cpl_url = self._search_regex('<script[^>]+src=(["\\\'])(?P<url>(?:/static|(?:https?:)?//static\\.beeg\\.com)/cpl/\\d+\\.js.*?)\\1', webpage, 'cpl', default=None, group='url')
    cpl_url = urljoin(url, cpl_url)
    (beeg_version, beeg_salt) = ([None] * 2)
    if cpl_url:
        cpl = self._download_webpage(self._proto_relative_url(cpl_url), video_id, 'Downloading cpl JS', fatal=False)
        if cpl:
            beeg_version = (int_or_none(self._search_regex('beeg_version\\s*=\\s*([^\\b]+)', cpl, 'beeg version', default=None)) or self._search_regex('/(\\d+)\\.js', cpl_url, 'beeg version', default=None))
            beeg_salt = self._search_regex('beeg_salt\\s*=\\s*(["\\\'])(?P<beeg_salt>.+?)\\1', cpl, 'beeg salt', default=None, group='beeg_salt')
    beeg_version = (beeg_version or '2185')
    beeg_salt = (beeg_salt or 'pmweAkq8lAYKdfWcFCUj0yoVgoPlinamH5UE1CB3H')
    video = self._download_json(('https://api.beeg.com/api/v6/%s/video/%s' % (beeg_version, video_id)), video_id)

    def split(o, e):

        def cut(s, x):
            n.append(s[:x])
            return s[x:]
        n = []
        r = (len(o) % e)
        if (r > 0):
            o = cut(o, r)
        while (len(o) > e):
            o = cut(o, e)
        n.append(o)
        return n

    def decrypt_key(key):
        a = beeg_salt
        e = compat_urllib_parse_unquote(key)
        o = ''.join([compat_chr((compat_ord(e[n]) - (compat_ord(a[(n % len(a))]) % 21))) for n in range(len(e))])
        return ''.join(split(o, 3)[::(- 1)])

    def decrypt_url(encrypted_url):
        encrypted_url = self._proto_relative_url(encrypted_url.replace('{DATA_MARKERS}', ''), 'https:')
        key = self._search_regex('/key=(.*?)%2Cend=', encrypted_url, 'key', default=None)
        if (not key):
            return encrypted_url
        return encrypted_url.replace(key, decrypt_key(key))
    formats = []
    for (format_id, video_url) in video.items():
        if (not video_url):
            continue
        height = self._search_regex('^(\\d+)[pP]$', format_id, 'height', default=None)
        if (not height):
            continue
        formats.append({
            'url': decrypt_url(video_url),
            'format_id': format_id,
            'height': int(height),
        })
    self._sort_formats(formats)
    title = video['title']
    video_id = (video.get('id') or video_id)
    display_id = video.get('code')
    description = video.get('desc')
    timestamp = parse_iso8601(video.get('date'), ' ')
    duration = int_or_none(video.get('duration'))
    tags = ([tag.strip() for tag in video['tags'].split(',')] if video.get('tags') else None)
    return {
        'id': video_id,
        'display_id': display_id,
        'title': title,
        'description': description,
        'timestamp': timestamp,
        'duration': duration,
        'tags': tags,
        'formats': formats,
        'age_limit': self._rta_search(webpage),
    }