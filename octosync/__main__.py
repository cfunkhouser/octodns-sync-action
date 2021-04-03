import fire

from . import action


def main():
    fire.Fire(action.sync_action, name='octosync')


if __name__ == '__main__':
    main()
