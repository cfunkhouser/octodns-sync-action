import contextlib
import io
import json
import os
import requests

from octodns import manager


_HTML_PROVIDER_CLASS = 'octodns.provider.plan.PlanHtml'

_PR_POST_USERNAME = 'octodns-sync-action'


class SyncActionManager(manager.Manager):
    """Manager which ensures certain configurations exist for nice Actions output.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # After super's __init__ is done, make sure there's a HTML plan output
        # provider configured to make it nice for GitHub actions output.
        try:
            if 'html' not in self.plan_outputs:
                _class = self._get_named_class(
                    'plan_output', _HTML_PROVIDER_CLASS)
                self.plan_outputs['html'] = _class(_HTML_PROVIDER_CLASS, **{})
        except TypeError:
            self.log.exception('Invalid plan_output config')
            raise manager.ManagerException(
                'Incorrect provider config for html')


def sync_action(octodns_config_file: str, /,
                doit: bool = False,
                post_pr_comment: bool = False):
    """Command to handle executing the octodns sync as a GitHub Action."""

    m: manager.Manager = None
    if post_pr_comment:
        m = SyncActionManager(octodns_config_file)
    else:
        m = manager.Manager(octodns_config_file)

    output_io = io.StringIO()
    with contextlib.redirect_stdout(output_io):
        m.sync(
            eligible_zones=[],
            eligible_sources=[],
            eligible_targets=[],
            dry_run=(not doit),
            # As of now, I can't imagine a good reason to allow this. If you
            # disagree with me, maybe explain your reasoning in the form of a
            # PR.
            force=False,
        )

    output = output_io.getvalue()
    if post_pr_comment:
        _try_posting_pr_comment(output)
    print(output)


def _try_posting_pr_comment(body: str, /) -> bool:
    user = _PR_POST_USERNAME
    token = os.environ.get('PR_COMMENT_TOKEN')
    if token is None:
        return False

    event_data_path = os.environ.get('GITHUB_EVENT_PATH')
    if event_data_path is None:
        return False

    comments_url = None
    try:
        with open(event_data_path, 'r') as event_data_file:
            event_data = json.load(event_data_file)
            comments_url = event_data['pull_request']['comments_url']
    except Exception:
        # Catch everything. If it didn't work, it didn't work.
        return False

    return _post_pr_comment(comments_url, user, token, body)


def _post_pr_comment(
        comments_url: str, user: str, token: str, body: str, /) -> bool:
    resp = requests.post(
        comments_url,
        auth=(user, token),
        json={
            'body': body,
        },
    )
    return int(resp.status_code / 100) == 2
