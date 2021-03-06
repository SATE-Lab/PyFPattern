def main():
    module = AnsibleModule(argument_spec=dict(username=dict(default=None), password=dict(default=None, no_log=True), host=dict(default='localhost'), port=dict(default='25'), sender=dict(default='root', aliases=['from']), to=dict(default='root', aliases=['recipients']), cc=dict(default=None), bcc=dict(default=None), subject=dict(required=True, aliases=['msg']), body=dict(default=None), attach=dict(default=None), headers=dict(default=None), charset=dict(default='us-ascii'), subtype=dict(default='plain')))
    username = module.params.get('username')
    password = module.params.get('password')
    host = module.params.get('host')
    port = module.params.get('port')
    sender = module.params.get('sender')
    recipients = module.params.get('to')
    copies = module.params.get('cc')
    blindcopies = module.params.get('bcc')
    subject = module.params.get('subject')
    body = module.params.get('body')
    attach_files = module.params.get('attach')
    headers = module.params.get('headers')
    charset = module.params.get('charset')
    subtype = module.params.get('subtype')
    (sender_phrase, sender_addr) = parseaddr(sender)
    if (not body):
        body = subject
    try:
        try:
            smtp = smtplib.SMTP_SSL(host, port=int(port))
        except (smtplib.SMTPException, ssl.SSLError):
            smtp = smtplib.SMTP(host, port=int(port))
    except Exception:
        e = get_exception()
        module.fail_json(rc=1, msg=('Failed to send mail to server %s on port %s: %s' % (host, port, e)))
    smtp.ehlo()
    if (username and password):
        if smtp.has_extn('STARTTLS'):
            smtp.starttls()
        try:
            smtp.login(username, password)
        except smtplib.SMTPAuthenticationError:
            module.fail_json(msg=('Authentication to %s:%s failed, please check your username and/or password' % (host, port)))
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = formataddr((sender_phrase, sender_addr))
    msg.preamble = 'Multipart message'
    if (headers is not None):
        for hdr in [x.strip() for x in headers.split('|')]:
            try:
                (h_key, h_val) = hdr.split('=')
                msg.add_header(h_key, h_val)
            except:
                pass
    if ('X-Mailer' not in msg):
        msg.add_header('X-Mailer', 'Ansible')
    to_list = []
    cc_list = []
    addr_list = []
    if (recipients is not None):
        for addr in [x.strip() for x in recipients.split(',')]:
            to_list.append(formataddr(parseaddr(addr)))
            addr_list.append(parseaddr(addr)[1])
    if (copies is not None):
        for addr in [x.strip() for x in copies.split(',')]:
            cc_list.append(formataddr(parseaddr(addr)))
            addr_list.append(parseaddr(addr)[1])
    if (blindcopies is not None):
        for addr in [x.strip() for x in blindcopies.split(',')]:
            addr_list.append(parseaddr(addr)[1])
    if (len(to_list) > 0):
        msg['To'] = ', '.join(to_list)
    if (len(cc_list) > 0):
        msg['Cc'] = ', '.join(cc_list)
    part = MIMEText((body + '\n\n'), _subtype=subtype, _charset=charset)
    msg.attach(part)
    if (attach_files is not None):
        for file in attach_files.split():
            try:
                fp = open(file, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(part)
                part.add_header('Content-disposition', 'attachment', filename=os.path.basename(file))
                msg.attach(part)
            except Exception:
                e = get_exception()
                module.fail_json(rc=1, msg=("Failed to send mail: can't attach file %s: %s" % (file, e)))
    composed = msg.as_string()
    try:
        smtp.sendmail(sender_addr, set(addr_list), composed)
    except Exception:
        e = get_exception()
        module.fail_json(rc=1, msg=('Failed to send mail to %s: %s' % (', '.join(addr_list), e)))
    smtp.quit()
    module.exit_json(changed=False)