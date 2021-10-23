def terminate_batch(connection, module, replace_instances, initial_instances, leftovers=False):
    batch_size = module.params.get('replace_batch_size')
    min_size = module.params.get('min_size')
    desired_capacity = module.params.get('desired_capacity')
    group_name = module.params.get('name')
    lc_check = module.params.get('lc_check')
    decrement_capacity = False
    break_loop = False
    as_group = connection.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])['AutoScalingGroups'][0]
    props = get_properties(as_group, module)
    desired_size = as_group['MinSize']
    (new_instances, old_instances) = get_instances_by_lc(props, lc_check, initial_instances)
    num_new_inst_needed = (desired_capacity - len(new_instances))
    instances_to_terminate = list_purgeable_instances(props, lc_check, replace_instances, initial_instances)
    log.debug('new instances needed: {0}'.format(num_new_inst_needed))
    log.debug('new instances: {0}'.format(new_instances))
    log.debug('old instances: {0}'.format(old_instances))
    log.debug('batch instances: {0}'.format(','.join(instances_to_terminate)))
    if (num_new_inst_needed == 0):
        decrement_capacity = True
        if (as_group['MinSize'] != min_size):
            connection.update_auto_scaling_group(AutoScalingGroupName=as_group['AutoScalingGroupName'], MinSize=min_size)
            log.debug('Updating minimum size back to original of {0}'.format(min_size))
        if leftovers:
            decrement_capacity = False
        break_loop = True
        instances_to_terminate = old_instances
        desired_size = min_size
        log.debug('No new instances needed')
    if ((num_new_inst_needed < batch_size) and (num_new_inst_needed != 0)):
        instances_to_terminate = instances_to_terminate[:num_new_inst_needed]
        decrement_capacity = False
        break_loop = False
        log.debug('{0} new instances needed'.format(num_new_inst_needed))
    log.debug('decrementing capacity: {0}'.format(decrement_capacity))
    for instance_id in instances_to_terminate:
        elb_dreg(connection, module, group_name, instance_id)
        log.debug('terminating instance: {0}'.format(instance_id))
        connection.terminate_instance_in_auto_scaling_group(InstanceId=instance_id, ShouldDecrementDesiredCapacity=decrement_capacity)
    return (break_loop, desired_size, instances_to_terminate)