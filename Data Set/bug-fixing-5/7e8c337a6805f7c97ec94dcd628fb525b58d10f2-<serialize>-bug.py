def serialize(self, name, f):
    '\n\n        :param name:\n        :param f:\n        :type f: file\n        :return:\n        '
    param = self.get(name)
    size = reduce((lambda a, b: (a * b)), param.shape)
    f.write(struct.pack('IIQ', 0, 4, size))
    param = param.astype(np.float32)
    f.write(param.tostring())