import argparse
from worker import Worker


def parse_args():
    parser = argparse.ArgumentParser(description='Starts an RQ worker.')
    parser.add_argument('-n', action='store', type=int, default=1,
            help='Number of concurrent threads.')
    parser.add_argument('-c', action='store', default=None,
            help='Concurrency backend. Should be "forking" (default) or "gevent".')
    return parser.parse_args()


def main():
    args = parse_args()
    print args

    w = Worker(type=args.c, num_processes=args.n)
    w.work()


if __name__ == '__main__':
    main()
