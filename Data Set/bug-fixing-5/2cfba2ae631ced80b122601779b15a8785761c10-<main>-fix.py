def main():
    parser = argparse.ArgumentParser(description='Chainer example: MNIST')
    parser.add_argument('--batchsize', '-b', type=int, default=100, help='Number of images in each mini-batch')
    parser.add_argument('--epoch', '-e', type=int, default=20, help='Number of sweeps over the dataset to train')
    parser.add_argument('--device', '-d', type=str, default='-1', help='Device specifier. Either ChainerX device specifier or an integer. If non-negative integer, CuPy arrays with specified device id are used. If negative integer, NumPy arrays are used')
    parser.add_argument('--out', '-o', default='result', help='Directory to output the result')
    parser.add_argument('--resume', '-r', default='', help='Resume the training from snapshot using model and state files in the specified directory')
    parser.add_argument('--unit', '-u', type=int, default=1000, help='Number of units')
    group = parser.add_argument_group('deprecated arguments')
    group.add_argument('--gpu', '-g', type=int, nargs='?', const=0, help='GPU ID (negative value indicates CPU)')
    args = parser.parse_args()
    device = parse_device(args)
    print('Device: {}'.format(device))
    print('# unit: {}'.format(args.unit))
    print('# Minibatch-size: {}'.format(args.batchsize))
    print('# epoch: {}'.format(args.epoch))
    print('')
    model = L.Classifier(train_mnist.MLP(args.unit, 10))
    model.to_device(device)
    device.use()
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)
    if args.resume:
        serializers.load_npz('{}/mlp.model'.format(args.resume), model)
        serializers.load_npz('{}/mlp.state'.format(args.resume), optimizer)
    (train, test) = chainer.datasets.get_mnist()
    train_count = len(train)
    test_count = len(test)
    train_iter = chainer.iterators.SerialIterator(train, args.batchsize)
    test_iter = chainer.iterators.SerialIterator(test, args.batchsize, repeat=False, shuffle=False)
    sum_accuracy = 0
    sum_loss = 0
    while (train_iter.epoch < args.epoch):
        batch = train_iter.next()
        (x, t) = convert.concat_examples(batch, device)
        optimizer.update(model, x, t)
        sum_loss += (float(model.loss.array) * len(t))
        sum_accuracy += (float(model.accuracy.array) * len(t))
        if train_iter.is_new_epoch:
            print('epoch: {}'.format(train_iter.epoch))
            print('train mean loss: {}, accuracy: {}'.format((sum_loss / train_count), (sum_accuracy / train_count)))
            sum_accuracy = 0
            sum_loss = 0
            with configuration.using_config('train', False):
                with chainer.using_config('enable_backprop', False):
                    for batch in test_iter:
                        (x, t) = convert.concat_examples(batch, device)
                        loss = model(x, t)
                        sum_loss += (float(loss.array) * len(t))
                        sum_accuracy += (float(model.accuracy.array) * len(t))
            test_iter.reset()
            print('test mean  loss: {}, accuracy: {}'.format((sum_loss / test_count), (sum_accuracy / test_count)))
            sum_accuracy = 0
            sum_loss = 0
    if (not os.path.exists(args.out)):
        os.makedirs(args.out)
    print('save the model')
    serializers.save_npz('{}/mlp.model'.format(args.out), model)
    print('save the optimizer')
    serializers.save_npz('{}/mlp.state'.format(args.out), optimizer)