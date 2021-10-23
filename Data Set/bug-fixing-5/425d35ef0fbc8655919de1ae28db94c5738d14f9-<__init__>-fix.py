def __init__(self, module, name, listeners=None, purge_listeners=None, zones=None, purge_zones=None, security_group_ids=None, health_check=None, subnets=None, purge_subnets=None, scheme='internet-facing', connection_draining_timeout=None, idle_timeout=None, cross_az_load_balancing=None, access_logs=None, stickiness=None, wait=None, wait_timeout=None, tags=None, region=None, instance_ids=None, purge_instance_ids=None, **aws_connect_params):
    self.module = module
    self.name = name
    self.listeners = listeners
    self.purge_listeners = purge_listeners
    self.instance_ids = instance_ids
    self.purge_instance_ids = purge_instance_ids
    self.zones = zones
    self.purge_zones = purge_zones
    self.security_group_ids = security_group_ids
    self.health_check = health_check
    self.subnets = subnets
    self.purge_subnets = purge_subnets
    self.scheme = scheme
    self.connection_draining_timeout = connection_draining_timeout
    self.idle_timeout = idle_timeout
    self.cross_az_load_balancing = cross_az_load_balancing
    self.access_logs = access_logs
    self.stickiness = stickiness
    self.wait = wait
    self.wait_timeout = wait_timeout
    self.tags = tags
    self.aws_connect_params = aws_connect_params
    self.region = region
    self.changed = False
    self.status = 'gone'
    self.elb_conn = self._get_elb_connection()
    try:
        self.elb = self._get_elb()
    except boto.exception.BotoServerError as e:
        module.fail_json(msg=('unable to get all load balancers: %s' % e.message), exception=traceback.format_exc())
    self.ec2_conn = self._get_ec2_connection()