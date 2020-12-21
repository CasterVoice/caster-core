import argparse
import logging
import sys

from castervoice.core import Controller


VERBOSITY_LOG_LEVEL = {
        0: 'WARNING',
        1: 'INFO',
        2: 'DEBUG'
}


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--verbose', '-v', action='count',
                        default=0, help='Verbose logging')

    return parser


def verify_parsed_args(args):
    max_verbose = len(VERBOSITY_LOG_LEVEL) - 1
    if args.verbose > max_verbose:
        raise ValueError("Maximum verbosity level is: -" + 'v'*max_verbose)

    return args


def get_args():
    args = get_parser().parse_args()
    try:
        return verify_parsed_args(args)
    except ValueError as error:
        print("Failed parsing arguments: ",
              error)
        sys.exit(1)


def main():
    """TODO: Docstring for main.

    :argv: TODO
    :returns: TODO

    """

    args = get_args()

    logging.basicConfig(level=VERBOSITY_LOG_LEVEL[args.verbose])

    controller = Controller.get()
    controller.listen()


if __name__ == "__main__":
    main()
