def set_token_value(self, token, value):
    if (len(value.split()) > 0):
        value = (('"' + value) + '"')
    if (self.platform == 'openbsd'):
        thiscmd = ('%s %s=%s' % (self.sysctl_cmd, token, value))
    elif (self.platform == 'freebsd'):
        ignore_missing = ''
        if self.args['ignoreerrors']:
            ignore_missing = '-i'
        thiscmd = ('%s %s %s=%s' % (self.sysctl_cmd, ignore_missing, token, value))
    else:
        ignore_missing = ''
        if self.args['ignoreerrors']:
            ignore_missing = '-e'
        thiscmd = ('%s %s -w %s=%s' % (self.sysctl_cmd, ignore_missing, token, value))
    (rc, out, err) = self.module.run_command(thiscmd)
    if (rc != 0):
        self.module.fail_json(msg=('setting %s failed: %s' % (token, (out + err))))
    else:
        return rc