def main():
    parser = argparse.ArgumentParser(description='Chainer example: VAE')
    parser.add_argument('--initmodel', '-m', type=str, help='Initialize the model from given file')
    parser.add_argument('--resume', '-r', type=str, help='Resume the optimization from snapshot')
    parser.add_argument('--device', '-d', type=str, default='-1', help='Device specifier. Either ChainerX device specifier or an integer. If non-negative integer, CuPy arrays with specified device id are used. If negative integer, NumPy arrays are used')
    parser.add_argument('--out', '-o', default='results', help='Directory to output the result')
    parser.add_argument('--epoch', '-e', default=100, type=int, help='number of epochs to learn')
    parser.add_argument('--dim-z', '-z', default=20, type=int, help='dimention of encoded vector')
    parser.add_argument('--dim-h', default=500, type=int, help='dimention of hidden layer')
    parser.add_argument('--beta', default=1.0, type=float, help='Regularization coefficient for the second term of ELBO bound')
    parser.add_argument('--k', '-k', default=1, type=int, help='Number of Monte Carlo samples used in encoded vector')
    parser.add_argument('--binary', action='store_true', help='Use binarized MNIST')
    parser.add_argument('--batch-size', '-b', type=int, default=100, help='learning minibatch size')
    parser.add_argument('--test', action='store_true', help='Use tiny datasets for quick tests')
    group = parser.add_argument_group('deprecated arguments')
    group.add_argument('--gpu', '-g', dest='device', type=int, nargs='?', const=0, help='GPU ID (negative value indicates CPU)')
    args = parser.parse_args()
    device = chainer.get_device(args.device)
    device.use()
    print('Device: {}'.format(device))
    print('# dim z: {}'.format(args.dim_z))
    print('# Minibatch-size: {}'.format(args.batch_size))
    print('# epoch: {}'.format(args.epoch))
    print('')
    encoder = net.make_encoder(784, args.dim_z, args.dim_h)
    decoder = net.make_decoder(784, args.dim_z, args.dim_h, binary_check=args.binary)
    prior = net.make_prior(args.dim_z)
    avg_elbo_loss = net.AvgELBOLoss(encoder, decoder, prior, beta=args.beta, k=args.k)
    avg_elbo_loss.to_device(device)
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(avg_elbo_loss)
    if (args.initmodel is not None):
        chainer.serializers.load_npz(args.initmodel, avg_elbo_loss)
    (train, test) = chainer.datasets.get_mnist(withlabel=False)
    if args.binary:
        train = (train >= 0.5).astype(np.float32)
        test = (test >= 0.5).astype(np.float32)
    if args.test:
        (train, _) = chainer.datasets.split_dataset(train, 100)
        (test, _) = chainer.datasets.split_dataset(test, 100)
    train_iter = chainer.iterators.SerialIterator(train, args.batch_size)
    test_iter = chainer.iterators.SerialIterator(test, args.batch_size, repeat=False, shuffle=False)
    updater = training.updaters.StandardUpdater(train_iter, optimizer, device=device, loss_func=avg_elbo_loss)
    trainer = training.Trainer(updater, (args.epoch, 'epoch'), out=args.out)
    trainer.extend(extensions.Evaluator(test_iter, avg_elbo_loss, device=device))
    if (device.xp is not chainerx):
        trainer.extend(extensions.DumpGraph('main/loss'))
    trainer.extend(extensions.snapshot(), trigger=(args.epoch, 'epoch'))
    trainer.extend(extensions.LogReport())
    trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'validation/main/loss', 'main/reconstr', 'main/kl_penalty', 'elapsed_time']))
    trainer.extend(extensions.ProgressBar())
    if (args.resume is not None):
        chainer.serializers.load_npz(args.resume, trainer)
    trainer.run()

    def save_images(x, filename):
        import matplotlib.pyplot as plt
        (fig, ax) = plt.subplots(3, 3, figsize=(9, 9), dpi=100)
        for (ai, xi) in zip(ax.flatten(), x):
            ai.imshow(xi.reshape(28, 28))
        fig.savefig(filename)
    avg_elbo_loss.to_cpu()
    train_ind = [1, 3, 5, 10, 2, 0, 13, 15, 17]
    x = chainer.Variable(np.asarray(train[train_ind]))
    with chainer.using_config('train', False), chainer.no_backprop_mode():
        x1 = decoder(encoder(x).mean, inference=True).mean
    save_images(x.array, os.path.join(args.out, 'train'))
    save_images(x1.array, os.path.join(args.out, 'train_reconstructed'))
    test_ind = [3, 2, 1, 18, 4, 8, 11, 17, 61]
    x = chainer.Variable(np.asarray(test[test_ind]))
    with chainer.using_config('train', False), chainer.no_backprop_mode():
        x1 = decoder(encoder(x).mean, inference=True).mean
    save_images(x.array, os.path.join(args.out, 'test'))
    save_images(x1.array, os.path.join(args.out, 'test_reconstructed'))
    z = prior().sample(9)
    x = decoder(z, inference=True).mean
    save_images(x.array, os.path.join(args.out, 'sampled'))