def _parse_cli_args(self):
    parser = argparse.ArgumentParser(description='Produce an Ansible Inventory file for an Azure subscription')
    parser.add_argument('--list', action='store_true', default=True, help='List instances (default: True)')
    parser.add_argument('--debug', action='store_true', default=False, help='Send debug messages to STDOUT')
    parser.add_argument('--host', action='store', help='Get all information about an instance')
    parser.add_argument('--pretty', action='store_true', default=False, help='Pretty print JSON output(default: False)')
    parser.add_argument('--profile', action='store', help='Azure profile contained in ~/.azure/credentials')
    parser.add_argument('--subscription_id', action='store', help='Azure Subscription Id')
    parser.add_argument('--client_id', action='store', help='Azure Client Id ')
    parser.add_argument('--secret', action='store', help='Azure Client Secret')
    parser.add_argument('--tenant', action='store', help='Azure Tenant Id')
    parser.add_argument('--ad_user', action='store', help='Active Directory User')
    parser.add_argument('--password', action='store', help='password')
    parser.add_argument('--adfs_authority_url', action='store', help='Azure ADFS authority url')
    parser.add_argument('--cloud_environment', action='store', help='Azure Cloud Environment name or metadata discovery URL')
    parser.add_argument('--resource-groups', action='store', help='Return inventory for comma separated list of resource group names')
    parser.add_argument('--tags', action='store', help='Return inventory for comma separated list of tag key:value pairs')
    parser.add_argument('--locations', action='store', help='Return inventory for comma separated list of locations')
    parser.add_argument('--no-powerstate', action='store_true', default=False, help='Do not include the power state of each virtual host')
    return parser.parse_args()