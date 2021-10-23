def delete_autoscaling_group(connection, module):
    group_name = module.params.get('name')
    notification_topic = module.params.get('notification_topic')
    wait_for_instances = module.params.get('wait_for_instances')
    wait_timeout = module.params.get('wait_timeout')
    if notification_topic:
        connection.delete_notification_configuration(AutoScalingGroupName=group_name, TopicARN=notification_topic)
    describe_response = connection.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])
    groups = describe_response.get('AutoScalingGroups')
    if groups:
        if (not wait_for_instances):
            connection.delete_auto_scaling_group(AutoScalingGroupName=group_name, ForceDelete=True)
            return True
        wait_timeout = (time.time() + wait_timeout)
        connection.update_auto_scaling_group(AutoScalingGroupName=group_name, MinSize=0, MaxSize=0, DesiredCapacity=0)
        instances = True
        while (instances and wait_for_instances and (wait_timeout >= time.time())):
            tmp_groups = connection.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name]).get('AutoScalingGroups')
            if tmp_groups:
                tmp_group = tmp_groups[0]
                if (not tmp_group.get('Instances')):
                    instances = False
            time.sleep(10)
        if (wait_timeout <= time.time()):
            module.fail_json(msg=('Waited too long for old instances to terminate. %s' % time.asctime()))
        connection.delete_auto_scaling_group(AutoScalingGroupName=group_name)
        while len(connection.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name]).get('AutoScalingGroups')):
            time.sleep(5)
        return True
    return False