

def setup_module_object():
    argument_spec = dict(name=dict(required=True), description=dict(), value=dict(required=False), state=dict(default='present', choices=['present', 'absent']), string_type=dict(default='String', choices=['String', 'StringList', 'SecureString']), decryption=dict(default=True, type='bool'), key_id=dict(default='alias/aws/ssm'), overwrite=dict(default=True, type='bool'), region=dict(required=False))
    return AnsibleAWSModule(argument_spec=argument_spec)
