def rcparam_role(name, rawtext, text, lineno, inliner, options={
    
}, content=[]):
    rendered = nodes.Text('rcParams["{}"]'.format(text))
    rel_source = inliner.document.attributes['source'].split('/doc/', 1)[1]
    levels = rel_source.count('/')
    refuri = (('../' * levels) + 'tutorials/introductory/customizing.html#matplotlib-rcparams')
    ref = nodes.reference(rawtext, rendered, refuri=refuri)
    return ([nodes.literal('', '', ref)], [])