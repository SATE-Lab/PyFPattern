

def managed_disk_to_dict(managed_disk):
    create_data = managed_disk.creation_data
    return dict(id=managed_disk.id, name=managed_disk.name, location=managed_disk.location, tags=managed_disk.tags, create_option=create_data.create_option.value.lower(), source_uri=create_data.source_uri, source_resource_uri=create_data.source_resource_id, disk_size_gb=managed_disk.disk_size_gb, os_type=(managed_disk.os_type.value if managed_disk.os_type else None), storage_account_type=managed_disk.sku.name.value, managed_by=managed_disk.managed_by)
