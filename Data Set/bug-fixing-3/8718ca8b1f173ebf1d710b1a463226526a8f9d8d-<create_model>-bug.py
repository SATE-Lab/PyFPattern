def create_model(lang, lex_attrs):
    lang_class = get_lang_class(lang)
    nlp = lang_class()
    for lexeme in nlp.vocab:
        lexeme.rank = 0
    lex_added = 0
    for attrs in lex_attrs:
        if ('settings' in attrs):
            continue
        lexeme = nlp.vocab[attrs['orth']]
        lexeme.set_attrs(**attrs)
        lexeme.is_oov = False
        lex_added += 1
        lex_added += 1
    oov_prob = min((lex.prob for lex in nlp.vocab))
    nlp.vocab.cfg.update({
        'oov_prob': (oov_prob - 1),
    })
    return nlp