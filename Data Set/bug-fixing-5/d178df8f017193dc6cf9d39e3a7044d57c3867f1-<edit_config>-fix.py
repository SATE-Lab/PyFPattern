@enable_mode
def edit_config(self, command):
    for cmd in chain(['configure terminal'], to_list(command), ['end']):
        try:
            cmd = ast.literal_eval(cmd)
            command = cmd['command']
            prompt = cmd['prompt']
            answer = cmd['answer']
            newline = cmd.get('newline', True)
        except:
            command = cmd
            prompt = None
            answer = None
            newline = True
        self.send_command(to_bytes(command), to_bytes(prompt), to_bytes(answer), False, newline)