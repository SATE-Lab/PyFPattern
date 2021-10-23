def _get_docker_remote_user(self):
    ' Get the default user configured in the docker container '
    p = subprocess.Popen([self.docker_cmd, 'inspect', '--format', '{{.Config.User}}', self._play_context.remote_addr], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    if (p.returncode != 0):
        display.warning((('unable to retrieve default user from docker container: %s' % out) + err))
        return None
    return (out.strip() or 'root')