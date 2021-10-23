def parse_args():
    parser = argparse.ArgumentParser('Fluid model benchmarks.')
    parser.add_argument('--model', type=str, choices=BENCHMARK_MODELS, default='resnet', help='The model to run benchmark with.')
    parser.add_argument('--batch_size', type=int, default=32, help='The minibatch size.')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='The learning rate.')
    parser.add_argument('--skip_batch_num', type=int, default=5, help='The first num of minibatch num to skip, for better performance test')
    parser.add_argument('--iterations', type=int, default=80, help='The number of minibatches.')
    parser.add_argument('--pass_num', type=int, default=100, help='The number of passes.')
    parser.add_argument('--data_format', type=str, default='NCHW', choices=['NCHW', 'NHWC'], help='The data data_format, now only support NCHW.')
    parser.add_argument('--device', type=str, default='GPU', choices=['CPU', 'GPU'], help='The device type.')
    parser.add_argument('--gpus', type=int, default=1, help='If gpus > 1, will use ParallelExecutor to run, else use Executor.')
    parser.add_argument('--data_set', type=str, default='flowers', choices=['cifar10', 'flowers'], help='Optional dataset for benchmark.')
    parser.add_argument('--infer_only', action='store_true', help='If set, run forward only.')
    parser.add_argument('--use_cprof', action='store_true', help='If set, use cProfile.')
    parser.add_argument('--use_nvprof', action='store_true', help='If set, use nvprof for CUDA.')
    parser.add_argument('--no_test', action='store_false', help='If set, test the testset during training.')
    parser.add_argument('--memory_optimize', action='store_true', help='If set, optimize runtime memory before start.')
    parser.add_argument('--use_fake_data', action='store_true', help='If set ommit the actual read data operators.')
    parser.add_argument('--profile', action='store_true', help='If set, profile a few steps.')
    parser.add_argument('--update_method', type=str, default='local', choices=['local', 'pserver', 'nccl2'], help='Choose parameter update method, can be local, pserver, nccl2.')
    args = parser.parse_args()
    return args