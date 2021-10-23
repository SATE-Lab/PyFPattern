def get_rules(meraki, net_id, number):
    path = meraki.construct_path('get_all', net_id=net_id)
    path = ((path + number) + '/l3FirewallRules')
    response = meraki.request(path, method='GET')
    if (meraki.status == 200):
        return response