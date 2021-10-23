def _exec(self, args, run_in_check_mode=False):
    if ((not self.module.check_mode) or (self.module.check_mode and run_in_check_mode)):
        cmd = [self._rabbitmqctl, '-q', '-n', self.node]
        (rc, out, err) = self.module.run_command((cmd + args), check_rc=True)
        return out.splitlines()
    return list()