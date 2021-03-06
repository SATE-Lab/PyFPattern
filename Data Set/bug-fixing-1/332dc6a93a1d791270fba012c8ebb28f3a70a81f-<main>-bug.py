

def main():
    skip = set([('test/sanity/code-smell/%s' % os.path.basename(__file__)), 'lib/ansible/module_utils/pycompat24.py'])
    basic_allow_once = True
    for path in (sys.argv[1:] or sys.stdin.read().splitlines()):
        if (path in skip):
            continue
        with open(path, 'r') as path_fd:
            for (line, text) in enumerate(path_fd.readlines()):
                match = re.search('(get_exception)', text)
                if match:
                    if ((path == 'lib/ansible/module_utils/basic.py') and basic_allow_once):
                        basic_allow_once = False
                        continue
                    print(('%s:%d:%d: do not use `get_exception`' % (path, (line + 1), (match.start(1) + 1))))
