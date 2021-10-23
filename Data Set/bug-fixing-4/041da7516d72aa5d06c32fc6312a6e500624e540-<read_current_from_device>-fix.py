def read_current_from_device(self):
    uri = 'https://{0}:{1}/mgmt/tm/gtm/server/{2}/virtual-servers/{3}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.server_name), transform_name(name=self.want.name))
    resp = self.client.api.get(uri)
    try:
        response = resp.json()
    except ValueError as ex:
        raise F5ModuleError(str(ex))
    if (('code' in response) and (response['code'] == 400)):
        if ('message' in response):
            raise F5ModuleError(response['message'])
        else:
            raise F5ModuleError(resp.content)
    return ApiParameters(params=response)