def terminate_batch(connection, replace_instances, initial_instances, leftovers=False):
    batch_size = module.params.get('replace_batch_size')
    min_size = module.params.get('min_size')
    desired_capacity = module.params.get('desired_capacity')
    group_name = module.params.get('name')
    lc_check = module.params.get('lc_check')
    decrement_capacity = False
    break_loop = False
    as_group = describe_autoscaling_groups(connection, group_name)[0]
    if (desired_capacity is None):
        desired_capacity = as_group['DesiredCapacity']
    props = get_properties(as_group)
    desired_size = as_group['MinSize']
    (new_instances, old_instances) = get_instances_by_lc(props, lc_check, initial_instances)
    num_new_inst_needed = (desired_capacity - len(new_instances))
    instances_to_terminate = list_purgeable_instances(props, lc_check, replace_instances, initial_instances)
    module.debug(('new instances needed: %s' % num_new_inst_needed))
    module.debug(('new instances: %s' % new_instances))
    module.debug(('old instances: %s' % old_instances))
    module.debug(('batch instances: %s' % ','.join(instances_to_terminate)))
    if (num_new_inst_needed == 0):
        decrement_capacity = True
        if (as_group['MinSize'] != min_size):
            updated_params = dict(AutoScalingGroupName=as_group['AutoScalingGroupName'], MinSize=min_size)
            update_asg(connection, **updated_params)
            module.debug(('Updating minimum size back to original of %s' % min_size))
        if leftovers:
            decrement_capacity = False
        break_loop = True
        instances_to_terminate = old_instances
        desired_size = min_size
        module.debug('No new instances needed')
    if ((num_new_inst_needed < batch_size) and (num_new_inst_needed != 0)):
        instances_to_terminate = instances_to_terminate[:num_new_inst_needed]
        decrement_capacity = False
        break_loop = False
        module.debug(('%s new instances needed' % num_new_inst_needed))
    module.debug(('decrementing capacity: %s' % decrement_capacity))
    for instance_id in instances_to_terminate:
        elb_dreg(connection, group_name, instance_id)
        module.debug(('terminating instance: %s' % instance_id))
        terminate_asg_instance(connection, instance_id, decrement_capacity)
    return (break_loop, desired_size, instances_to_terminate)