def _to_lines(self, stdout):
    lines = list()
    for item in stdout:
        if isinstance(item, string_types):
            item = item.split('\n')
        lines.append(item)
    return lines