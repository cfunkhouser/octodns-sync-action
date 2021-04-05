import fire
import logging

from . import action


def main():
    logging.getLogger('').setLevel(logging.DEBUG)
    fire.Fire(action.sync_action, name='octosync')


if __name__ == '__main__':
    main()
