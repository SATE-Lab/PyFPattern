

def list(self):
    policies = self._exec(['list_policies'], True)
    for policy in policies:
        if (not policy):
            continue
        policy_name = policy.split('\t')[1]
        if (policy_name == self._name):
            return True
    return False
