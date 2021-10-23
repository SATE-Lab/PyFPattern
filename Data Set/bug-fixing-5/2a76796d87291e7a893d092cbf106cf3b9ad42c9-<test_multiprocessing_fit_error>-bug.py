@skip_generators
def test_multiprocessing_fit_error():
    arr_data = np.random.randint(0, 256, (50, 2))
    arr_labels = np.random.randint(0, 2, 50)
    batch_size = 10
    n_samples = 50
    good_batches = 3

    @threadsafe_generator
    def custom_generator(use_weights=False):
        'Raises an exception after a few good batches'
        for i in range(good_batches):
            batch_index = np.random.randint(0, (n_samples - batch_size))
            start = batch_index
            end = (start + batch_size)
            X = arr_data[start:end]
            y = arr_labels[start:end]
            (yield (X, y))
        raise RuntimeError
    model = Sequential()
    model.add(Dense(1, input_shape=(2,)))
    model.compile(loss='mse', optimizer='adadelta')
    samples = (batch_size * (good_batches + 1))
    if (os.name is 'nt'):
        with pytest.raises(RuntimeError):
            model.fit_generator(custom_generator(), steps_per_epoch=samples, validation_steps=None, max_queue_size=10, workers=WORKERS, use_multiprocessing=True)
    else:
        with pytest.raises(RuntimeError):
            model.fit_generator(custom_generator(), steps_per_epoch=samples, validation_steps=None, max_queue_size=10, workers=WORKERS, use_multiprocessing=True)
    if (os.name is 'nt'):
        with pytest.raises(RuntimeError):
            model.fit_generator(custom_generator(), steps_per_epoch=samples, validation_steps=None, max_queue_size=10, workers=1, use_multiprocessing=True)
    else:
        with pytest.raises(RuntimeError):
            model.fit_generator(custom_generator(), steps_per_epoch=samples, validation_steps=None, max_queue_size=10, workers=1, use_multiprocessing=True)
    with pytest.raises(RuntimeError):
        model.fit_generator(custom_generator(), steps_per_epoch=samples, validation_steps=None, max_queue_size=10, workers=0, use_multiprocessing=True)