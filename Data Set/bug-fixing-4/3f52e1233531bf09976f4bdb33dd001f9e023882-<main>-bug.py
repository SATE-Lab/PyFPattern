@plac.annotations(lang='ISO language code', in_dir='Location of input directory', out_loc='Location of output file', n_workers=('Number of workers', 'option', 'n', int), size=('Dimension of the word vectors', 'option', 'd', int), window=('Context window size', 'option', 'w', int), min_count=('Min count', 'option', 'm', int), negative=('Number of negative samples', 'option', 'g', int), nr_iter=('Number of iterations', 'option', 'i', int))
def main(lang, in_dir, out_loc, negative=5, n_workers=4, window=5, size=128, min_count=10, nr_iter=2):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = Word2Vec(size=size, window=window, min_count=min_count, workers=n_workers, sample=1e-05, negative=negative)
    nlp = spacy.blank(lang)
    corpus = Corpus(in_dir)
    total_words = 0
    total_sents = 0
    for (text_no, text_loc) in enumerate(iter_dir(corpus.directory)):
        with text_loc.open('r', encoding='utf-8') as file_:
            text = file_.read()
        total_sents += text.count('\n')
        doc = nlp(text)
        total_words += corpus.count_doc(doc)
        logger.info('PROGRESS: at batch #%i, processed %i words, keeping %i word types', text_no, total_words, len(corpus.strings))
    model.corpus_count = total_sents
    model.raw_vocab = defaultdict(int)
    for (orth, freq) in corpus.counts:
        if (freq >= min_count):
            model.raw_vocab[nlp.vocab.strings[orth]] = freq
    model.scale_vocab()
    model.finalize_vocab()
    model.iter = nr_iter
    model.train(corpus)
    model.save(out_loc)