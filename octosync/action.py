from octodns import manager


_HTML_PROVIDER_CLASS = 'octodns.provider.plan.PlanHtml'


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


def sync_action(config_file: str, /, doit: bool = False):
    """Command to handle executing the octodns sync as a GitHub Action."""
    m = SyncActionManager(config_file)
    m.sync(
        eligible_zones=[],
        eligible_sources=[],
        eligible_targets=[],
        dry_run=(not doit),
        force=False,
    )
