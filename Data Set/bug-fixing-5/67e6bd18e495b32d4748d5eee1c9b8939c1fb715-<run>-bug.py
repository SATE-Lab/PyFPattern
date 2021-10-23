def run(self, tmp=None, task_vars=None):
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    if self._play_context.check_mode:
        result['skipped'] = True
        return result
    executable = self._task.args.get('executable')
    result.update(self._low_level_execute_command(self._task.args.get('_raw_params'), executable=executable))
    return result