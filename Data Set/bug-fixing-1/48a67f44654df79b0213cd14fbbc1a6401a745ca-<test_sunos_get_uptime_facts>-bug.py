

def test_sunos_get_uptime_facts(mocker):
    kstat_output = '\nunix:0:system_misc:boot_time\t1548249689\n'
    module_mock = mocker.patch('ansible.module_utils.basic.AnsibleModule')
    module = module_mock()
    module.run_command.return_value = (0, kstat_output, '')
    inst = sunos.SunOSHardware(module)
    expected = (int(time.time()) - 1548249689)
    result = inst.get_uptime_facts()
    assert (expected == result['uptime_seconds'])
