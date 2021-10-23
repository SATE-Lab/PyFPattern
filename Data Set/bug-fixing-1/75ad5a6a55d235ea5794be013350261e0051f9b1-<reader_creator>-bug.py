

def reader_creator(data_file, label_file, setid_file, dataset_name, mapper, buffered_size=1024, use_xmap=True):
    '\n    1. read images from tar file and\n        merge images into batch files in 102flowers.tgz_batch/\n    2. get a reader to read sample from batch file\n\n    :param data_file: downloaded data file\n    :type data_file: string\n    :param label_file: downloaded label file\n    :type label_file: string\n    :param setid_file: downloaded setid file containing information\n                        about how to split dataset\n    :type setid_file: string\n    :param dataset_name: data set name (tstid|trnid|valid)\n    :type dataset_name: string\n    :param mapper: a function to map image bytes data to type\n                    needed by model input layer\n    :type mapper: callable\n    :param buffered_size: the size of buffer used to process images\n    :type buffered_size: int\n    :return: data reader\n    :rtype: callable\n    '
    labels = scio.loadmat(label_file)['labels'][0]
    indexes = scio.loadmat(setid_file)[dataset_name][0]
    img2label = {
        
    }
    for i in indexes:
        img = ('jpg/image_%05d.jpg' % i)
        img2label[img] = labels[(i - 1)]
    file_list = batch_images_from_tar(data_file, dataset_name, img2label)

    def reader():
        for file in open(file_list):
            file = file.strip()
            batch = None
            with open(file, 'r') as f:
                batch = cPickle.load(f)
            data = batch['data']
            labels = batch['label']
            for (sample, label) in itertools.izip(data, batch['label']):
                (yield (sample, int(label)))
    if use_xmap:
        return xmap_readers(mapper, reader, cpu_count(), buffered_size)
    else:
        return map_readers(mapper, reader)
