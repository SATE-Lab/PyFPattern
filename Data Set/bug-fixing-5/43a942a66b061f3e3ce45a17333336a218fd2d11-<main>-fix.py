def main():
    parser = argparse.ArgumentParser(description='Chainer example: DCGAN')
    parser.add_argument('--batchsize', '-b', type=int, default=50, help='Number of images in each mini-batch')
    parser.add_argument('--epoch', '-e', type=int, default=1000, help='Number of sweeps over the dataset to train')
    parser.add_argument('--device', '-d', type=str, default='-1', help='Device specifier. Either ChainerX device specifier or an integer. If non-negative integer, CuPy arrays with specified device id are used. If negative integer, NumPy arrays are used')
    parser.add_argument('--dataset', '-i', default='', help='Directory of image files.  Default is cifar-10.')
    parser.add_argument('--out', '-o', default='result', help='Directory to output the result')
    parser.add_argument('--resume', '-r', type=str, help='Resume the training from snapshot')
    parser.add_argument('--n_hidden', '-n', type=int, default=100, help='Number of hidden units (z)')
    parser.add_argument('--seed', type=int, default=0, help='Random seed of z at visualization stage')
    parser.add_argument('--snapshot_interval', type=int, default=1000, help='Interval of snapshot')
    parser.add_argument('--display_interval', type=int, default=100, help='Interval of displaying log to console')
    group = parser.add_argument_group('deprecated arguments')
    group.add_argument('--gpu', '-g', dest='device', type=int, nargs='?', const=0, help='GPU ID (negative value indicates CPU)')
    args = parser.parse_args()
    if (chainer.get_dtype() == numpy.float16):
        warnings.warn('This example may cause NaN in FP16 mode.', RuntimeWarning)
    device = chainer.get_device(args.device)
    device.use()
    print('Device: {}'.format(device))
    print('# Minibatch-size: {}'.format(args.batchsize))
    print('# n_hidden: {}'.format(args.n_hidden))
    print('# epoch: {}'.format(args.epoch))
    print('')
    gen = Generator(n_hidden=args.n_hidden)
    dis = Discriminator()
    gen.to_device(device)
    dis.to_device(device)

    def make_optimizer(model, alpha=0.0002, beta1=0.5):
        optimizer = chainer.optimizers.Adam(alpha=alpha, beta1=beta1)
        optimizer.setup(model)
        optimizer.add_hook(chainer.optimizer_hooks.WeightDecay(0.0001), 'hook_dec')
        return optimizer
    opt_gen = make_optimizer(gen)
    opt_dis = make_optimizer(dis)
    if (args.dataset == ''):
        (train, _) = chainer.datasets.get_cifar10(withlabel=False, scale=255.0)
    else:
        all_files = os.listdir(args.dataset)
        image_files = [f for f in all_files if (('png' in f) or ('jpg' in f))]
        print('{} contains {} image files'.format(args.dataset, len(image_files)))
        train = chainer.datasets.ImageDataset(paths=image_files, root=args.dataset)
    train_iter = chainer.iterators.SerialIterator(train, args.batchsize)
    updater = DCGANUpdater(models=(gen, dis), iterator=train_iter, optimizer={
        'gen': opt_gen,
        'dis': opt_dis,
    }, device=device)
    trainer = training.Trainer(updater, (args.epoch, 'epoch'), out=args.out)
    snapshot_interval = (args.snapshot_interval, 'iteration')
    display_interval = (args.display_interval, 'iteration')
    trainer.extend(extensions.snapshot(filename='snapshot_iter_{.updater.iteration}.npz'), trigger=snapshot_interval)
    trainer.extend(extensions.snapshot_object(gen, 'gen_iter_{.updater.iteration}.npz'), trigger=snapshot_interval)
    trainer.extend(extensions.snapshot_object(dis, 'dis_iter_{.updater.iteration}.npz'), trigger=snapshot_interval)
    trainer.extend(extensions.LogReport(trigger=display_interval))
    trainer.extend(extensions.PrintReport(['epoch', 'iteration', 'gen/loss', 'dis/loss']), trigger=display_interval)
    trainer.extend(extensions.ProgressBar(update_interval=10))
    trainer.extend(out_generated_image(gen, dis, 10, 10, args.seed, args.out), trigger=snapshot_interval)
    if (args.resume is not None):
        chainer.serializers.load_npz(args.resume, trainer)
    trainer.run()