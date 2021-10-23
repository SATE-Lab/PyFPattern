

def save_inference_model(self, executor, dirname, feeded_var_names=None, target_vars=None, main_program=None, export_for_deployment=True):
    '\n        save pserver model called from a worker\n\n        Args:\n            executor(Executor): fluid executor\n            dirname(str): save model path\n            feeded_var_names(list): default None\n            target_vars(list): default None\n            main_program(Program): default None\n            export_for_deployment(bool): default None\n\n        Examples:\n            .. code-block:: python\n\n              fleet.save_inference_model(dirname="hdfs:/my/path")\n\n        '
    self._fleet_ptr.save_model(dirname, 0)
