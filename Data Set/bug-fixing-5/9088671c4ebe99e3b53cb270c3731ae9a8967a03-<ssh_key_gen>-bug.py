def ssh_key_gen(self):
    info = self.user_info()
    try:
        ssh_key_file = self.get_ssh_key_path()
    except Exception as e:
        return (1, '', to_native(e))
    ssh_dir = os.path.dirname(ssh_key_file)
    if (not os.path.exists(ssh_dir)):
        if self.module.check_mode:
            return (0, '', '')
        try:
            os.mkdir(ssh_dir, int('0700', 8))
            os.chown(ssh_dir, info[2], info[3])
        except OSError as e:
            return (1, '', ('Failed to create %s: %s' % (ssh_dir, to_native(e))))
    if os.path.exists(ssh_key_file):
        return (None, 'Key already exists', '')
    cmd = [self.module.get_bin_path('ssh-keygen', True)]
    cmd.append('-t')
    cmd.append(self.ssh_type)
    if (self.ssh_bits > 0):
        cmd.append('-b')
        cmd.append(self.ssh_bits)
    cmd.append('-C')
    cmd.append(self.ssh_comment)
    cmd.append('-f')
    cmd.append(ssh_key_file)
    if (self.ssh_passphrase is not None):
        if self.module.check_mode:
            self.module.debug(('In check mode, would have run: "%s"' % cmd))
            return (0, '', '')
        (master_in_fd, slave_in_fd) = pty.openpty()
        (master_out_fd, slave_out_fd) = pty.openpty()
        (master_err_fd, slave_err_fd) = pty.openpty()
        env = os.environ.copy()
        env['LC_ALL'] = 'C'
        try:
            p = subprocess.Popen([to_bytes(c) for c in cmd], stdin=slave_in_fd, stdout=slave_out_fd, stderr=slave_err_fd, preexec_fn=os.setsid, env=env)
            out_buffer = b''
            err_buffer = b''
            while (p.poll() is None):
                (r, w, e) = select.select([master_out_fd, master_err_fd], [], [], 1)
                first_prompt = b'Enter passphrase (empty for no passphrase):'
                second_prompt = b'Enter same passphrase again'
                prompt = first_prompt
                for fd in r:
                    if (fd == master_out_fd):
                        chunk = os.read(master_out_fd, 10240)
                        out_buffer += chunk
                        if (prompt in out_buffer):
                            os.write(master_in_fd, (self.ssh_passphrase + b'\r'))
                            prompt = second_prompt
                    else:
                        chunk = os.read(master_err_fd, 10240)
                        err_buffer += chunk
                        if (prompt in err_buffer):
                            os.write(master_in_fd, (self.ssh_passphrase + b'\r'))
                            prompt = second_prompt
                    if ((b'Overwrite (y/n)?' in out_buffer) or (b'Overwrite (y/n)?' in err_buffer)):
                        return (None, 'Key already exists', '')
            rc = p.returncode
            out = to_native(out_buffer)
            err = to_native(err_buffer)
        except OSError as e:
            return (1, '', to_native(e))
    else:
        cmd.append('-N')
        cmd.append('')
        (rc, out, err) = self.execute_command(cmd)
    if ((rc == 0) and (not self.module.check_mode)):
        os.chown(ssh_key_file, info[2], info[3])
        os.chown(('%s.pub' % ssh_key_file), info[2], info[3])
    return (rc, out, err)