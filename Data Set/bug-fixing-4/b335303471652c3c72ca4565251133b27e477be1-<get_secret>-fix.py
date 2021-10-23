def get_secret(self, name, version=''):
    ' Gets an existing secret '
    secret_bundle = self.client.get_secret(self.keyvault_uri, name, version)
    if secret_bundle:
        secret_id = KeyVaultId.parse_secret_id(secret_bundle.id)
        return dict(secret_id=secret_id.id, secret_value=secret_bundle.value)
    return None