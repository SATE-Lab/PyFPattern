def get_volumes(module, ssid, api_url, user, pwd, mappable):
    volumes = ('storage-systems/%s/%s' % (ssid, mappable))
    url = (api_url + volumes)
    try:
        (rc, data) = request(url, url_username=user, url_password=pwd)
    except Exception:
        err = get_exception()
        module.fail_json(msg=('Failed to mappable objects. Type[%s. Id [%s]. Error [%s].' % (mappable, ssid, str(err))))
    return data