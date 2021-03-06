

def build_custom_checkers(by_lang):
    RuleList = List[Dict[(str, Any)]]

    def custom_check_file(fn, rules, skip_rules=None, max_length=None):
        failed = False
        line_tups = []
        for (i, line) in enumerate(open(fn)):
            line_newline_stripped = line.strip('\n')
            line_fully_stripped = line_newline_stripped.strip()
            skip = False
            for rule in (skip_rules or []):
                if re.match(rule, line):
                    skip = True
            if line_fully_stripped.endswith('  # nolint'):
                continue
            if skip:
                continue
            tup = (i, line, line_newline_stripped, line_fully_stripped)
            line_tups.append(tup)
        rules_to_apply = []
        fn_dirname = os.path.dirname(fn)
        for rule in rules:
            exclude_list = rule.get('exclude', set())
            if ((fn in exclude_list) or (fn_dirname in exclude_list)):
                continue
            if rule.get('include_only'):
                found = False
                for item in rule.get('include_only', set()):
                    if (item in fn):
                        found = True
                if (not found):
                    continue
            rules_to_apply.append(rule)
        for rule in rules_to_apply:
            exclude_lines = {line for (exclude_fn, line) in rule.get('exclude_line', set()) if (exclude_fn == fn)}
            pattern = rule['pattern']
            for (i, line, line_newline_stripped, line_fully_stripped) in line_tups:
                if (line_fully_stripped in exclude_lines):
                    exclude_lines.remove(line_fully_stripped)
                    continue
                try:
                    line_to_check = line_fully_stripped
                    if (rule.get('strip') is not None):
                        if (rule['strip'] == '\n'):
                            line_to_check = line_newline_stripped
                        else:
                            raise Exception('Invalid strip rule')
                    if re.search(pattern, line_to_check):
                        sys.stdout.write((rule['description'] + (' at %s line %s:\n' % (fn, (i + 1)))))
                        print(line)
                        failed = True
                except Exception:
                    print(('Exception with %s at %s line %s' % (rule['pattern'], fn, (i + 1))))
                    traceback.print_exc()
            if exclude_lines:
                print(('Please remove exclusions for file %s: %s' % (fn, exclude_lines)))
        lastLine = None
        for (i, line, line_newline_stripped, line_fully_stripped) in line_tups:
            if isinstance(line, bytes):
                line_length = len(line.decode('utf-8'))
            else:
                line_length = len(line)
            if ((max_length is not None) and (line_length > max_length) and ('# type' not in line) and ('test' not in fn) and ('example' not in fn) and (not re.match('\\[[ A-Za-z0-9_:,&()-]*\\]: http.*', line)) and (not re.match('`\\{\\{ external_api_uri_subdomain \\}\\}[^`]+`', line)) and ('#ignorelongline' not in line) and ('migrations' not in fn)):
                print(('Line too long (%s) at %s line %s: %s' % (len(line), fn, (i + 1), line_newline_stripped)))
                failed = True
            lastLine = line
        if (lastLine and ('\n' not in lastLine)):
            print(("No newline at the end of file.  Fix with `sed -i '$a\\' %s`" % (fn,)))
            failed = True
        return failed
    whitespace_rules = [{
        'pattern': '\\s+$',
        'strip': '\n',
        'description': 'Fix trailing whitespace',
    }, {
        'pattern': '\t',
        'strip': '\n',
        'exclude': set(['zerver/lib/bugdown/codehilite.py', 'tools/travis/success-http-headers.txt']),
        'description': 'Fix tab-based whitespace',
    }]
    markdown_whitespace_rules = (list([rule for rule in whitespace_rules if (rule['pattern'] != '\\s+$')]) + [{
        'pattern': '((?<!\\s)\\s$)|(\\s\\s\\s+$)|(^\\s+$)',
        'strip': '\n',
        'description': 'Fix trailing whitespace',
    }, {
        'pattern': '^#+[A-Za-z0-9]',
        'strip': '\n',
        'description': 'Missing space after # in heading',
    }])
    js_rules = (cast(RuleList, [{
        'pattern': '[^_]function\\(',
        'description': 'The keyword "function" should be followed by a space',
    }, {
        'pattern': '.*blueslip.warning\\(.*',
        'description': 'The module blueslip has no function warning, try using blueslip.warn',
    }, {
        'pattern': '[)]{$',
        'description': 'Missing space between ) and {',
    }, {
        'pattern': '["\']json/',
        'description': 'Relative URL for JSON route not supported by i18n',
    }, {
        'pattern': (' =' + '[^ =>~"]'),
        'description': 'Missing whitespace after "="',
    }, {
        'pattern': '^[ ]*//[A-Za-z0-9]',
        'description': 'Missing space after // in comment',
    }, {
        'pattern': 'if[(]',
        'description': 'Missing space between if and (',
    }, {
        'pattern': 'else{$',
        'description': 'Missing space between else and {',
    }, {
        'pattern': '^else {$',
        'description': 'Write JS else statements on same line as }',
    }, {
        'pattern': '^else if',
        'description': 'Write JS else statements on same line as }',
    }, {
        'pattern': 'console[.][a-z]',
        'exclude': set(['static/js/blueslip.js', 'frontend_tests/zjsunit', 'frontend_tests/casper_lib/common.js', 'frontend_tests/node_tests', 'static/js/debug.js']),
        'description': 'console.log and similar should not be used in webapp',
    }, {
        'pattern': 'i18n[.]t',
        'include_only': set(['static/js/portico/']),
        'description': 'i18n.t is not available in portico pages yet',
    }, {
        'pattern': '[.]text\\(["\'][a-zA-Z]',
        'description': 'Strings passed to $().text should be wrapped in i18n.t() for internationalization',
    }, {
        'pattern': 'compose_error\\(["\']',
        'description': 'Argument to compose_error should be a literal string enclosed by i18n.t()',
    }, {
        'pattern': 'ui.report_success\\(',
        'description': 'Deprecated function, use ui_report.success.',
    }, {
        'pattern': 'report.success\\(["\']',
        'description': 'Argument to report_success should be a literal string enclosed by i18n.t()',
    }, {
        'pattern': 'ui.report_error\\(',
        'description': 'Deprecated function, use ui_report.error.',
    }, {
        'pattern': 'report.error\\(["\']',
        'description': 'Argument to report_error should be a literal string enclosed by i18n.t()',
    }]) + whitespace_rules)
    python_rules = (cast(RuleList, [{
        'pattern': '^(?!#)@login_required',
        'description': '@login_required is unsupported; use @zulip_login_required',
    }, {
        'pattern': '".*"%\\([a-z_].*\\)?$',
        'description': 'Missing space around "%"',
    }, {
        'pattern': "'.*'%\\([a-z_].*\\)?$",
        'exclude': set(['analytics/lib/counts.py', 'analytics/tests/test_counts.py']),
        'exclude_line': set([('zerver/views/users.py', 'return json_error(_("Email \'%(email)s\' not allowed for realm \'%(realm)s\'") %'), ('zproject/settings.py', "'format': '%(asctime)s %(levelname)-8s %(message)s'"), ('static/templates/settings/bot-settings.handlebars', "'https://hostname.example.com/bots/followup'")]),
        'description': 'Missing space around "%"',
    }, {
        'pattern': (' =' + '[^ =>~"]'),
        'description': 'Missing whitespace after "="',
    }, {
        'pattern': '":\\w[^"]*$',
        'description': 'Missing whitespace after ":"',
    }, {
        'pattern': "':\\w[^']*$",
        'description': 'Missing whitespace after ":"',
    }, {
        'pattern': '^\\s+[#]\\w',
        'strip': '\n',
        'description': 'Missing whitespace after "#"',
    }, {
        'pattern': 'assertEquals[(]',
        'description': 'Use assertEqual, not assertEquals (which is deprecated).',
    }, {
        'pattern': '== None',
        'description': 'Use `is None` to check whether something is None',
    }, {
        'pattern': 'type:[(]',
        'description': 'Missing whitespace after ":" in type annotation',
    }, {
        'pattern': '# type [(]',
        'description': 'Missing : after type in type annotation',
    }, {
        'pattern': '#type',
        'description': 'Missing whitespace after "#" in type annotation',
    }, {
        'pattern': 'if[(]',
        'description': 'Missing space between if and (',
    }, {
        'pattern': ', [)]',
        'description': 'Unnecessary whitespace between "," and ")"',
    }, {
        'pattern': '%  [(]',
        'description': 'Unnecessary whitespace between "%" and "("',
    }, {
        'pattern': ' % [a-zA-Z0-9_.]*\\)?$',
        'exclude_line': set([('tools/tests/test_template_parser.py', '{% foo')]),
        'description': 'Used % comprehension without a tuple',
    }, {
        'pattern': '.*%s.* % \\([a-zA-Z0-9_.]*\\)$',
        'description': 'Used % comprehension without a tuple',
    }, {
        'pattern': 'django.utils.translation',
        'include_only': set(['test/']),
        'description': 'Test strings should not be tagged for translationx',
    }, {
        'pattern': 'json_success\\({}\\)',
        'description': 'Use json_success() to return nothing',
    }, {
        'pattern': '\\Wjson_error\\(_\\(?\\w+\\)',
        'exclude': set(['zerver/tests']),
        'description': 'Argument to json_error should be a literal string enclosed by _()',
    }, {
        'pattern': '\\Wjson_error\\([\'"].+[),]$',
        'exclude': set(['zerver/tests']),
        'exclude_line': set([('zerver/views/compatibility.py', 'return json_error("Client is too old")')]),
        'description': 'Argument to json_error should a literal string enclosed by _()',
    }, {
        'pattern': '\\WJsonableError\\(_\\(?\\w.+\\)',
        'exclude': set(['zerver/tests']),
        'description': 'Argument to JsonableError should be a literal string enclosed by _()',
    }, {
        'pattern': '\\WJsonableError\\(["\'].+\\)',
        'exclude': set(['zerver/tests']),
        'description': 'Argument to JsonableError should be a literal string enclosed by _()',
    }, {
        'pattern': '([a-zA-Z0-9_]+)=REQ\\([\'"]\\1[\'"]',
        'description': "REQ's first argument already defaults to parameter name",
    }, {
        'pattern': 'self\\.client\\.(get|post|patch|put|delete)',
        'exclude': set(['zilencer/tests.py']),
        'description': 'Do not call self.client directly for put/patch/post/get.\n    See WRAPPER_COMMENT in test_helpers.py for details.\n    ',
    }, {
        'pattern': '[^r][M]essage.objects.get',
        'exclude': set(['zerver/tests', 'zerver/worker/queue_processors.py']),
        'description': 'Please use access_message() to fetch Message objects',
    }, {
        'pattern': '[S]tream.objects.get',
        'include_only': set(['zerver/views/']),
        'description': 'Please use access_stream_by_*() to fetch Stream objects',
    }, {
        'pattern': 'get_stream[(]',
        'include_only': set(['zerver/views/', 'zerver/lib/actions.py']),
        'exclude': set(['zerver/views/messages.py']),
        'exclude_line': set([('zerver/lib/actions.py', 'get_stream(new_name, stream.realm)'), ('zerver/lib/actions.py', 'stream = get_stream(stream_name, realm)'), ('zerver/lib/actions.py', 'get_stream(signups_stream, admin_realm)')]),
        'description': 'Please use access_stream_by_*() to fetch Stream objects',
    }, {
        'pattern': '[S]tream.objects.filter',
        'include_only': set(['zerver/views/']),
        'description': 'Please use access_stream_by_*() to fetch Stream objects',
    }, {
        'pattern': '^from (zerver|analytics|confirmation)',
        'include_only': set(['/migrations/']),
        'exclude': set(['zerver/migrations/0032_verify_all_medium_avatar_images.py', 'zerver/migrations/0041_create_attachments_for_old_messages.py', 'zerver/migrations/0060_move_avatars_to_be_uid_based.py']),
        'description': "Don't import models or other code in migrations; see docs/schema-migrations.md",
    }, {
        'pattern': 'datetime[.](now|utcnow)',
        'include_only': set(['zerver/', 'analytics/']),
        'description': "Don't use datetime in backend code.\nSee https://zulip.readthedocs.io/en/latest/code-style.html#naive-datetime-objects",
    }, {
        'pattern': 'render_to_response\\(',
        'description': 'Use render() instead of render_to_response().',
    }, {
        'pattern': 'python[23]',
        'exclude': set(['tools/lib/provision.py', 'tools/setup/setup_venvs.py', 'scripts/lib/setup_venv.py']),
        'description': 'Explicit python invocations should not include a version',
    }, {
        'pattern': '(^|\\s)open\\s*\\(',
        'description': "open() should not be used in Zulip's bots. Use functions provided by the bots framework to access the filesystem.",
        'include_only': set(['api/bots/']),
        'exclude': set(['api/bots/john/john.py']),
    }]) + whitespace_rules)
    bash_rules = ([{
        'pattern': '#!.*sh [-xe]',
        'description': 'Fix shebang line with proper call to /usr/bin/env for Bash path, change -x|-e switches to set -x|set -e',
    }] + whitespace_rules[0:1])
    css_rules = (cast(RuleList, [{
        'pattern': '^[^:]*:\\S[^:]*;$',
        'description': 'Missing whitespace after : in CSS',
    }, {
        'pattern': '[a-z]{',
        'description': "Missing whitespace before '{' in CSS.",
    }, {
        'pattern': 'https://',
        'description': 'Zulip CSS should have no dependencies on external resources',
    }, {
        'pattern': '^[ ][ ][a-zA-Z0-9]',
        'description': 'Incorrect 2-space indentation in CSS',
        'exclude': set(['static/third/thirdparty-fonts.css']),
        'strip': '\n',
    }, {
        'pattern': '{\\w',
        'description': "Missing whitespace after '{' in CSS (should be newline).",
    }, {
        'pattern': ' thin[; ]',
        'description': 'thin CSS attribute is under-specified, please use 1px.',
    }, {
        'pattern': ' medium[; ]',
        'description': 'medium CSS attribute is under-specified, please use pixels.',
    }, {
        'pattern': ' thick[; ]',
        'description': 'thick CSS attribute is under-specified, please use pixels.',
    }]) + whitespace_rules)
    prose_style_rules = [{
        'pattern': '[^\\/\\#\\-"]([jJ]avascript)',
        'description': 'javascript should be spelled JavaScript',
    }, {
        'pattern': '[^\\/\\-\\."\'\\_\\=\\>]([gG]ithub)[^\\.\\-\\_"\\<]',
        'description': 'github should be spelled GitHub',
    }, {
        'pattern': '[oO]rganisation',
        'description': 'Organization is spelled with a z',
    }, {
        'pattern': '!!! warning',
        'description': "!!! warning is invalid; it's spelled '!!! warn'",
    }]
    html_rules = ((whitespace_rules + prose_style_rules) + [{
        'pattern': 'placeholder="[^{]',
        'description': '`placeholder` value should be translatable.',
        'exclude_line': [('templates/zerver/register.html', 'placeholder="acme"'), ('templates/zerver/register.html', 'placeholder="Acme"'), ('static/templates/settings/realm-domains-modal.handlebars', '<td><input type="text" class="new-realm-domain" placeholder="acme.com"></input></td>')],
        'exclude': set(['static/templates/settings/emoji-settings-admin.handlebars', 'static/templates/settings/realm-filter-settings-admin.handlebars', 'static/templates/settings/bot-settings.handlebars']),
    }, {
        'pattern': "placeholder='[^{]",
        'description': '`placeholder` value should be translatable.',
    }, {
        'pattern': 'script src="http',
        'description': "Don't directly load dependencies from CDNs.  See docs/front-end-build-process.md",
    }, {
        'pattern': "title='[^{]",
        'description': '`title` value should be translatable.',
    }, {
        'pattern': 'title="[^{\\:]',
        'exclude_line': set([('templates/zerver/markdown_help.html', '<td><img alt=":heart:" class="emoji" src="/static/generated/emoji/images/emoji/heart.png" title=":heart:" /></td>')]),
        'exclude': set(['templates/zerver/emails']),
        'description': '`title` value should be translatable.',
    }, {
        'pattern': '\\Walt=["\'][^{"\']',
        'description': 'alt argument should be enclosed by _() or it should be an empty string.',
        'exclude': set(['static/templates/settings/display-settings.handlebars', 'templates/zerver/keyboard_shortcuts.html', 'templates/zerver/markdown_help.html']),
    }, {
        'pattern': '\\Walt=["\']{{ ?["\']',
        'description': 'alt argument should be enclosed by _().',
    }])
    handlebars_rules = (html_rules + [{
        'pattern': '[<]script',
        'description': 'Do not use inline <script> tags here; put JavaScript in static/js instead.',
    }, {
        'pattern': "{{t '.*' }}[\\.\\?!]",
        'description': 'Period should be part of the translatable string.',
    }, {
        'pattern': '{{t ".*" }}[\\.\\?!]',
        'description': 'Period should be part of the translatable string.',
    }, {
        'pattern': '{{/tr}}[\\.\\?!]',
        'description': 'Period should be part of the translatable string.',
    }])
    jinja2_rules = (html_rules + [{
        'pattern': '{% endtrans %}[\\.\\?!]',
        'description': 'Period should be part of the translatable string.',
    }, {
        'pattern': '{{ _(.+) }}[\\.\\?!]',
        'description': 'Period should be part of the translatable string.',
    }])
    json_rules = []
    markdown_rules = ((markdown_whitespace_rules + prose_style_rules) + [{
        'pattern': '\\[(?P<url>[^\\]]+)\\]\\((?P=url)\\)',
        'description': 'Linkified markdown URLs should use cleaner <http://example.com> syntax.',
    }])
    help_markdown_rules = (markdown_rules + [{
        'pattern': '[a-z][.][A-Z]',
        'description': 'Likely missing space after end of sentence',
    }, {
        'pattern': '[rR]ealm',
        'description': 'Realms are referred to as Organizations in user-facing docs.',
    }])
    txt_rules = whitespace_rules

    def check_custom_checks_py():
        failed = False
        for fn in by_lang['py']:
            if ('custom_check.py' in fn):
                continue
            if custom_check_file(fn, python_rules, max_length=140):
                failed = True
        return failed

    def check_custom_checks_nonpy():
        failed = False
        for fn in by_lang['js']:
            if custom_check_file(fn, js_rules):
                failed = True
        for fn in by_lang['sh']:
            if custom_check_file(fn, bash_rules):
                failed = True
        for fn in by_lang['css']:
            if custom_check_file(fn, css_rules):
                failed = True
        for fn in by_lang['handlebars']:
            if custom_check_file(fn, handlebars_rules):
                failed = True
        for fn in by_lang['html']:
            if custom_check_file(fn, jinja2_rules):
                failed = True
        for fn in by_lang['json']:
            if custom_check_file(fn, json_rules):
                failed = True
        markdown_docs_length_exclude = {'api/bots/converter/readme.md', 'docs/bots-guide.md', 'docs/dev-env-first-time-contributors.md', 'docs/webhook-walkthrough.md', 'docs/life-of-a-request.md', 'docs/logging.md', 'docs/migration-renumbering.md', 'docs/readme-symlink.md', 'README.md', 'zerver/webhooks/helloworld/doc.md', 'zerver/webhooks/trello/doc.md'}
        for fn in by_lang['md']:
            max_length = None
            if (fn not in markdown_docs_length_exclude):
                max_length = 120
            rules = markdown_rules
            if fn.startswith('templates/zerver/help'):
                rules = help_markdown_rules
            if custom_check_file(fn, rules, max_length=max_length):
                failed = True
        for fn in (by_lang['txt'] + by_lang['text']):
            if custom_check_file(fn, txt_rules):
                failed = True
        for fn in by_lang['yaml']:
            if custom_check_file(fn, txt_rules):
                failed = True
        return failed
    return (check_custom_checks_py, check_custom_checks_nonpy)
