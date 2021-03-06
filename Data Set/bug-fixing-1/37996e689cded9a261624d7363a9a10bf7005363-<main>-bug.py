

def main():
    current_datetime = '{}'.format(datetime.datetime.today())
    parser = argparse.ArgumentParser(description='Chainer example: Text Classification')
    parser.add_argument('--batchsize', '-b', type=int, default=64, help='Number of images in each mini-batch')
    parser.add_argument('--epoch', '-e', type=int, default=30, help='Number of sweeps over the dataset to train')
    parser.add_argument('--device', '-d', type=str, default='-1', help='Device specifier. Either ChainerX device specifier or an integer. If non-negative integer, CuPy arrays with specified device id are used. If negative integer, NumPy arrays are used')
    parser.add_argument('--out', '-o', default='result', help='Directory to output the result')
    parser.add_argument('--resume', '-r', type=str, help='Resume the training from snapshot')
    parser.add_argument('--unit', '-u', type=int, default=300, help='Number of units')
    parser.add_argument('--layer', '-l', type=int, default=1, help='Number of layers of RNN or MLP following CNN')
    parser.add_argument('--dropout', type=float, default=0.4, help='Dropout rate')
    parser.add_argument('--dataset', '-data', default='imdb.binary', choices=['dbpedia', 'imdb.binary', 'imdb.fine', 'TREC', 'stsa.binary', 'stsa.fine', 'custrev', 'mpqa', 'rt-polarity', 'subj'], help='Name of dataset.')
    parser.add_argument('--model', '-model', default='cnn', choices=['cnn', 'rnn', 'bow'], help='Name of encoder model type.')
    parser.add_argument('--char-based', action='store_true')
    parser.add_argument('--test', dest='test', action='store_true')
    parser.set_defaults(test=False)
    group = parser.add_argument_group('deprecated arguments')
    group.add_argument('--gpu', '-g', dest='device', type=int, nargs='?', const=0, help='GPU ID (negative value indicates CPU)')
    args = parser.parse_args()
    print(json.dumps(args.__dict__, indent=2))
    device = chainer.get_device(args.device)
    device.use()
    if (args.dataset == 'dbpedia'):
        (train, test, vocab) = text_datasets.get_dbpedia(char_based=args.char_based)
    elif args.dataset.startswith('imdb.'):
        (train, test, vocab) = text_datasets.get_imdb(fine_grained=args.dataset.endswith('.fine'), char_based=args.char_based)
    elif (args.dataset in ['TREC', 'stsa.binary', 'stsa.fine', 'custrev', 'mpqa', 'rt-polarity', 'subj']):
        (train, test, vocab) = text_datasets.get_other_text_dataset(args.dataset, char_based=args.char_based)
    if args.test:
        train = train[:100]
        test = test[:100]
    print('Device: {}'.format(device))
    print('# train data: {}'.format(len(train)))
    print('# test  data: {}'.format(len(test)))
    print('# vocab: {}'.format(len(vocab)))
    n_class = len(set([int(d[1]) for d in train]))
    print('# class: {}'.format(n_class))
    train_iter = chainer.iterators.SerialIterator(train, args.batchsize)
    test_iter = chainer.iterators.SerialIterator(test, args.batchsize, repeat=False, shuffle=False)
    if (args.model == 'rnn'):
        Encoder = nets.RNNEncoder
    elif (args.model == 'cnn'):
        Encoder = nets.CNNEncoder
    elif (args.model == 'bow'):
        Encoder = nets.BOWMLPEncoder
    encoder = Encoder(n_layers=args.layer, n_vocab=len(vocab), n_units=args.unit, dropout=args.dropout)
    model = nets.TextClassifier(encoder, n_class)
    model.to_device(device)
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)
    optimizer.add_hook(chainer.optimizer.WeightDecay(0.0001))
    updater = training.updaters.StandardUpdater(train_iter, optimizer, converter=convert_seq, device=device)
    trainer = training.Trainer(updater, (args.epoch, 'epoch'), out=args.out)
    trainer.extend(extensions.Evaluator(test_iter, model, converter=convert_seq, device=device))
    record_trigger = training.triggers.MaxValueTrigger('validation/main/accuracy', (1, 'epoch'))
    trainer.extend(extensions.snapshot(filename='snapshot_epoch_{.updater.epoch}'), trigger=record_trigger)
    trainer.extend(extensions.snapshot_object(model, 'best_model.npz'), trigger=record_trigger)
    trainer.extend(extensions.LogReport())
    trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'validation/main/loss', 'main/accuracy', 'validation/main/accuracy', 'elapsed_time']))
    trainer.extend(extensions.ProgressBar())
    if (not os.path.isdir(args.out)):
        os.mkdir(args.out)
    vocab_path = os.path.join(args.out, 'vocab.json')
    with open(vocab_path, 'w') as f:
        json.dump(vocab, f)
    model_path = os.path.join(args.out, 'best_model.npz')
    model_setup = args.__dict__
    model_setup['vocab_path'] = vocab_path
    model_setup['model_path'] = model_path
    model_setup['n_class'] = n_class
    model_setup['datetime'] = current_datetime
    with open(os.path.join(args.out, 'args.json'), 'w') as f:
        json.dump(args.__dict__, f)
    if (args.resume is not None):
        chainer.serializers.load_npz(args.resume, trainer)
    trainer.run()
