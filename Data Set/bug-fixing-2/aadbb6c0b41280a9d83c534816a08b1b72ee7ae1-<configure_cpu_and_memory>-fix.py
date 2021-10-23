

def configure_cpu_and_memory(self, vm_obj, vm_creation=False):
    if ('hardware' in self.params):
        if ('num_cpus' in self.params['hardware']):
            try:
                num_cpus = int(self.params['hardware']['num_cpus'])
            except ValueError as e:
                self.module.fail_json(msg='hardware.num_cpus attribute should be an integer value.')
            if ('num_cpu_cores_per_socket' in self.params['hardware']):
                try:
                    num_cpu_cores_per_socket = int(self.params['hardware']['num_cpu_cores_per_socket'])
                except ValueError as e:
                    self.module.fail_json(msg='hardware.num_cpu_cores_per_socket attribute should be an integer value.')
                if ((num_cpus % num_cpu_cores_per_socket) != 0):
                    self.module.fail_json(msg='hardware.num_cpus attribute should be a multiple of hardware.num_cpu_cores_per_socket')
                self.configspec.numCoresPerSocket = num_cpu_cores_per_socket
                if ((vm_obj is None) or (self.configspec.numCoresPerSocket != vm_obj.config.hardware.numCoresPerSocket)):
                    self.change_detected = True
            self.configspec.numCPUs = num_cpus
            if ((vm_obj is None) or (self.configspec.numCPUs != vm_obj.config.hardware.numCPU)):
                self.change_detected = True
        elif (vm_creation and (not self.params['template'])):
            self.module.fail_json(msg='hardware.num_cpus attribute is mandatory for VM creation')
        if ('memory_mb' in self.params['hardware']):
            try:
                self.configspec.memoryMB = int(self.params['hardware']['memory_mb'])
            except ValueError:
                self.module.fail_json(msg='Failed to parse hardware.memory_mb value. Please refer the documentation and provide correct value.')
            if ((vm_obj is None) or (self.configspec.memoryMB != vm_obj.config.hardware.memoryMB)):
                self.change_detected = True
        elif (vm_creation and (not self.params['template'])):
            self.module.fail_json(msg='hardware.memory_mb attribute is mandatory for VM creation')
        if ('hotadd_memory' in self.params['hardware']):
            self.configspec.memoryHotAddEnabled = bool(self.params['hardware']['hotadd_memory'])
            if ((vm_obj is None) or (self.configspec.memoryHotAddEnabled != vm_obj.config.memoryHotAddEnabled)):
                self.change_detected = True
        if ('hotadd_cpu' in self.params['hardware']):
            self.configspec.cpuHotAddEnabled = bool(self.params['hardware']['hotadd_cpu'])
            if ((vm_obj is None) or (self.configspec.cpuHotAddEnabled != vm_obj.config.cpuHotAddEnabled)):
                self.change_detected = True
        if ('hotremove_cpu' in self.params['hardware']):
            self.configspec.cpuHotRemoveEnabled = bool(self.params['hardware']['hotremove_cpu'])
            if ((vm_obj is None) or (self.configspec.cpuHotRemoveEnabled != vm_obj.config.cpuHotRemoveEnabled)):
                self.change_detected = True
        if ('memory_reservation' in self.params['hardware']):
            memory_reservation_mb = 0
            try:
                memory_reservation_mb = int(self.params['hardware']['memory_reservation'])
            except ValueError as e:
                self.module.fail_json(msg=('Failed to set memory_reservation value.Valid value for memory_reservation value in MB (integer): %s' % e))
            mem_alloc = vim.ResourceAllocationInfo()
            mem_alloc.reservation = memory_reservation_mb
            self.configspec.memoryAllocation = mem_alloc
            if ((vm_obj is None) or (self.configspec.memoryAllocation.reservation != vm_obj.config.memoryAllocation.reservation)):
                self.change_detected = True
        if ('memory_reservation_lock' in self.params['hardware']):
            self.configspec.memoryReservationLockedToMax = bool(self.params['hardware']['memory_reservation_lock'])
            if ((vm_obj is None) or (self.configspec.memoryReservationLockedToMax != vm_obj.config.memoryReservationLockedToMax)):
                self.change_detected = True
