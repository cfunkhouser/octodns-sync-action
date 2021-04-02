import fire

from . import action


def main():
    fire.Fire(action.SyncAction, name='action')


if __name__ == '__main__':
    main()
