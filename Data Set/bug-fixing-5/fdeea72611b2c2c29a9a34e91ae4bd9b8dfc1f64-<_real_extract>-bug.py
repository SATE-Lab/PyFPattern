def _real_extract(self, url):
    video_id = self._match_id(url)
    self._set_cookie('cda.pl', 'cda.player', 'html5')
    webpage = self._download_webpage(((self._BASE_URL + '/video/') + video_id), video_id)
    if ('Ten film jest dostępny dla użytkowników premium' in webpage):
        raise ExtractorError('This video is only available for premium users.', expected=True)
    formats = []
    uploader = self._search_regex('(?x)\n            <(span|meta)[^>]+itemprop=(["\\\'])author\\2[^>]*>\n            (?:<\\1[^>]*>[^<]*</\\1>|(?!</\\1>)(?:.|\\n))*?\n            <(span|meta)[^>]+itemprop=(["\\\'])name\\4[^>]*>(?P<uploader>[^<]+)</\\3>\n        ', webpage, 'uploader', default=None, group='uploader')
    view_count = self._search_regex('Odsłony:(?:\\s|&nbsp;)*([0-9]+)', webpage, 'view_count', default=None)
    average_rating = self._search_regex('<(?:span|meta)[^>]+itemprop=(["\\\'])ratingValue\\1[^>]*>(?P<rating_value>[0-9.]+)', webpage, 'rating', fatal=False, group='rating_value')
    info_dict = {
        'id': video_id,
        'title': self._og_search_title(webpage),
        'description': self._og_search_description(webpage),
        'uploader': uploader,
        'view_count': int_or_none(view_count),
        'average_rating': float_or_none(average_rating),
        'thumbnail': self._og_search_thumbnail(webpage),
        'formats': formats,
        'duration': None,
    }

    def extract_format(page, version):
        json_str = self._search_regex('player_data=(\\\\?["\\\'])(?P<player_data>.+?)\\1', page, ('%s player_json' % version), fatal=False, group='player_data')
        if (not json_str):
            return
        player_data = self._parse_json(json_str, ('%s player_data' % version), fatal=False)
        if (not player_data):
            return
        video = player_data.get('video')
        if ((not video) or ('file' not in video)):
            self.report_warning(('Unable to extract %s version information' % version))
            return
        f = {
            'url': video['file'],
        }
        m = re.search('<a[^>]+data-quality="(?P<format_id>[^"]+)"[^>]+href="[^"]+"[^>]+class="[^"]*quality-btn-active[^"]*">(?P<height>[0-9]+)p', page)
        if m:
            f.update({
                'format_id': m.group('format_id'),
                'height': int(m.group('height')),
            })
        info_dict['formats'].append(f)
        if (not info_dict['duration']):
            info_dict['duration'] = parse_duration(video.get('duration'))
    extract_format(webpage, 'default')
    for (href, resolution) in re.findall('<a[^>]+data-quality="[^"]+"[^>]+href="([^"]+)"[^>]+class="quality-btn"[^>]*>([0-9]+p)', webpage):
        webpage = self._download_webpage((self._BASE_URL + href), video_id, ('Downloading %s version information' % resolution), fatal=False)
        if (not webpage):
            self.report_warning(('Unable to download %s version information' % resolution))
            continue
        extract_format(webpage, resolution)
    self._sort_formats(formats)
    return info_dict