

def build_entity(self):
    storage_type = self._get_storage_type()
    storage = self._get_storage()
    self._login(storage_type, storage)
    return otypes.StorageDomain(name=self._module.params['name'], description=self._module.params['description'], comment=self._module.params['comment'], type=otypes.StorageDomainType(self._module.params['domain_function']), host=otypes.Host(name=self._module.params['host']), storage=(otypes.HostStorage(type=otypes.StorageType(storage_type), logical_units=([otypes.LogicalUnit(id=lun_id, address=storage.get('address'), port=storage.get('port', 3260), target=storage.get('target'), username=storage.get('username'), password=storage.get('password')) for lun_id in (storage.get('lun_id') if isinstance(storage.get('lun_id'), list) else [storage.get('lun_id')])] if (storage_type in ['iscsi', 'fcp']) else None), override_luns=storage.get('override_luns'), mount_options=storage.get('mount_options'), vfs_type=('glusterfs' if (storage_type in ['glusterfs']) else storage.get('vfs_type')), address=storage.get('address'), path=storage.get('path'), nfs_retrans=storage.get('retrans'), nfs_timeo=storage.get('timeout'), nfs_version=(otypes.NfsVersion(storage.get('version')) if storage.get('version') else None)) if (storage_type is not None) else None))
