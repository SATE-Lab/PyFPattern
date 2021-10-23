def _run_findmnt(self, findmnt_path):
    args = ['--list', '--noheadings', '--notruncate']
    cmd = ([findmnt_path] + args)
    (rc, out, err) = self.module.run_command(cmd, errors='surrogate_or_replace')
    return (rc, out, err)