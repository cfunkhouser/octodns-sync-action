import io
import json
import logging
import os
import requests
import typing

from octodns import manager


_MD_PROVIDER_CLASS = 'octodns.provider.plan.PlanMarkdown'

LOG = logging.getLogger('octosync')


class SyncActionManager(manager.Manager):
    """Manager which ensures certain configurations exist for nice Actions output.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # After super's __init__ is done, reset the plan outputs (effectively
        # ignoring any configured in the configuration file) and set up a
        # single Markdown plan output provider.
        self.plan_outputs = {}
        try:
            _class = self._get_named_class(
                'plan_output', _MD_PROVIDER_CLASS)
            self.plan_outputs['markdown'] = _class(_MD_PROVIDER_CLASS, **{})
        except Exception:
            self.log.exception('Failed to configure plan output provider.')
            raise manager.ManagerException(
                'Failed to configure plan output provider.')


# Parsing boolean values is annoying in Python, and Fire is no exception.
# See: github.com/google/python-fire/blob/master/docs/guide.md#boolean-arguments # noqa: E501
def _sanitize_bool(val: typing.Any, /) -> bool:
    """Sanitize argument values to boolean."""
    if isinstance(val, str):
        return val.lower() == 'true'
    return bool(val)


def sync_action(octodns_config_file: str, /,
                doit: bool = False,
                post_pr_comment: bool = False):
    """Command to handle executing the octodns sync as a GitHub Action."""

    doit = _sanitize_bool(doit)
    post_pr_comment = _sanitize_bool(post_pr_comment)

    logging.debug(
        f'octodns_config_file ({type(octodns_config_file)}) = '
        f'{octodns_config_file}, '
        f'doit ({type(doit)}) = {doit}, '
        f'post_pr_comment ({type(post_pr_comment)}) = {post_pr_comment}')

    output_io = io.StringIO()
    SyncActionManager(octodns_config_file).sync(
        eligible_zones=[],
        eligible_sources=[],
        eligible_targets=[],
        dry_run=(not doit),
        # As of now, I can't imagine a good reason to allow forcing. If you
        # disagree with me, maybe explain your reasoning in the form of a
        # PR.
        force=False,
        plan_output_fh=output_io,
    )

    if post_pr_comment:
        _try_posting_pr_comment(output_io.getvalue())


def _try_posting_pr_comment(body: str, /) -> bool:
    token = os.environ.get('GITHUB_TOKEN')
    if token is None:
        logging.warn('No GITHUB_TOKEN, cannot continue')
        return False

    event_data_path = os.environ.get('GITHUB_EVENT_PATH')
    if event_data_path is None:
        logging.warn('No GITHUB_EVENT_PATH, cannot continue')
        return False

    comments_url = None
    try:
        with open(event_data_path, 'r') as event_data_file:
            event_data = json.load(event_data_file)
            comments_url = event_data['pull_request']['comments_url']
        logging.info(f'Good news, everyone! comments_url = {comments_url}')
    except Exception as e:
        # Catch everything. If it didn't work, it didn't work.
        logging.exception(e)
        return False

    return _post_pr_comment(comments_url, token, body)


def _post_pr_comment(
        comments_url: str, token: str, body: str, /) -> bool:

    logging.debug(f'Attempting to post:\n{body}')

    resp = requests.post(
        comments_url,
        headers={
            "Accept": "application/vnd.github.v3+json",
        },
        # Username will be overridden by GitHub, but cannot be blank.
        auth=('doesntmatter', token),
        json={
            'body': body,
        },
    )

    logging.info(f'PR Comment Post Response: {resp}')
    logging.debug(f'Full Response Payload:\n{resp.text}')

    return int(resp.status_code / 100) == 2
