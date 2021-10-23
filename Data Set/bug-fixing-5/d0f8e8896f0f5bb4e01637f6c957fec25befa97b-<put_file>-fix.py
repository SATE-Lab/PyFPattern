def put_file(self, in_path, out_path):
    'Put file.'
    super(Connection, self).put_file(in_path, out_path)
    if (not exists(to_bytes(in_path, errors='surrogate_or_strict'))):
        raise AnsibleFileNotFound(("file or module does not exist: '%s'" % to_native(in_path)))
    try:
        put_url = self.fileManager.InitiateFileTransferToGuest(vm=self.vm, auth=self.vm_auth, guestFilePath=out_path, fileAttributes=vim.GuestFileAttributes(), fileSize=getsize(in_path), overwrite=True)
    except vim.fault.NoPermission as e:
        raise AnsibleError(('No Permission Error: %s %s' % (to_native(e.msg), to_native(e.privilegeId))))
    except vmodl.fault.SystemError as e:
        if (e.reason == 'vix error codes = (3016, 0).\n'):
            raise AnsibleConnectionFailure(('Connection failed, is the vm currently rebooting? Reason: %s' % to_native(e.reason)))
        else:
            raise AnsibleConnectionFailure(('Connection failed. Reason %s' % to_native(e.reason)))
    except vim.fault.GuestOperationsUnavailable:
        raise AnsibleConnectionFailure('Cannot connect to guest. Native error: GuestOperationsUnavailable')
    url = self._fix_url_for_hosts(put_url)
    with open(in_path, 'rb') as fd:
        response = requests.put(url, verify=self.validate_certs, data=fd)
    if (response.status_code != 200):
        raise AnsibleError('File transfer failed')