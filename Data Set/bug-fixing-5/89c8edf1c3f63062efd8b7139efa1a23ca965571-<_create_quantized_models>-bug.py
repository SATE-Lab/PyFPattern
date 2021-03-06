def _create_quantized_models(name, sym_prefix):

    def func(pretrained=False, tag=None, root='~/.mxnet/models', ctx=cpu(0), **kwargs):
        'Quantized model.\n\n        Parameters\n        ----------\n        pretrained : bool or str\n            Boolean value controls whether to load the default pretrained weights for model.\n            String value represents the hashtag for a certain version of pretrained weights.\n        tag : str, default is None\n            Optional length-8 sha1sum of parameter file. If `None`, best parameter file\n            will be used.\n        ctx : Context, default CPU\n            The context in which to load the pretrained weights.\n        root : str, default $MXNET_HOME/models\n            Location for keeping the model parameters.\n        '
        from ..model_zoo import get_model
        from ..model_store import get_model_file
        curr_dir = os.path.abspath(os.path.dirname(__file__))
        model_name = name.replace('mobilenet1_', 'mobilenet1.')
        model_name = model_name.replace('mobilenet0_', 'mobilenet0.')
        json_file = os.path.join(curr_dir, '{}-symbol.json'.format(model_name))
        base_name = '_'.join(model_name.split('_')[:(- 1)])
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            param_file = (get_model_file(base_name, tag=tag, root=root) if pretrained else None)
            net = get_model('_'.join(model_name.split('_')[:(- 1)]), prefix=sym_prefix)
            classes = getattr(net, 'classes', [])
            sym_net = SymbolBlock.imports(json_file, ['data'], None, ctx=ctx)
            if param_file:
                import tempfile
                net.load_params(param_file)
                net.hybridize()
                if ('512' in base_name):
                    net(mx.nd.zeros((1, 3, 512, 512)))
                elif ('300' in base_name):
                    net(mx.nd.zeros((1, 3, 300, 300)))
                else:
                    net(mx.nd.zeros((1, 3, 224, 224)))
                with tempfile.TemporaryDirectory() as tmpdirname:
                    prefix = os.path.join(tmpdirname, 'tmp')
                    net.export(prefix, epoch=0)
                    param_prefix = (prefix + '-0000.params')
                    sym_net.collect_params().load(param_prefix)
        net.classes = classes
        net.reset_class = _not_impl
        net.set_nms = _not_impl
        return net
    func.__name__ = name
    globals()[name] = func