import argparse
import logging
import sys

from castervoice.core import Controller


VERBOSITY_LOG_LEVEL = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG
}

DEFAULT_CONFIG_DIR = "config"


def _on_begin():
    print("Speech start detected.")


def _on_recognition(words, rule, node):
    print(u"Recognized: %s" % u" ".join(words))
    print(u"    Executing rule: %s" % (rule))
    print(u"    Action: %s" % (node.value()))


def _on_failure():
    print("Sorry, what was that?")


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--verbose', '-v', action='count',
                        default=0, help='Verbose logging')

    parser.add_argument('--config-dir', '-c', default=DEFAULT_CONFIG_DIR,
                        help='Configuration directory')

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

    controller = Controller(args.config_dir)
    if args.verbose > 0:
        controller.listen(_on_begin, _on_recognition, _on_failure)
    else:
        controller.listen()


if __name__ == "__main__":
    main()
