def override_blacklist(*ip_addresses):

    def decorator(func):

        def wrapper(*args, **kwargs):
            disallowed_ips = frozenset(net_socket.DISALLOWED_IPS)
            net_socket.DISALLOWED_IPS = frozenset((ipaddress.ip_network(six.text_type(ip)) for ip in ip_addresses))
            func(*args, **kwargs)
            net_socket.DISALLOWED_IPS = disallowed_ips
        return wrapper
    return decorator