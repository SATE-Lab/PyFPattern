

def load_batch(fpath, label_key='labels'):
    f = open(fpath, 'rb')
    if (sys.version_info < (3,)):
        d = cPickle.load(f)
    else:
        d = cPickle.load(f, encoding='bytes')
        for (k, v) in d.items():
            del d[k]
            d[k.decode('utf8')] = v
    f.close()
    data = d['data']
    labels = d[label_key]
    data = data.reshape(data.shape[0], 3, 32, 32)
    return (data, labels)
