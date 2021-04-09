# octodns-sync-action

A GitHub action to publish DNS changes from a GitHub repository to any supported
cloud provider using github.com/github/octodns.

This is compatible with the OctoDNS `SplitYamlProvider`.

## Example Workflows

### Publish Changes on Push to `main`

```yaml
name: cloudflare-dns-sync
on:
  # Publish changes to Cloudflare when files matching the specified patterns are
  # pushed to main.
  push:
    branches:
      - main
    paths:
      - "config/to-cloudflare.yaml"
      - "zones/*.yaml"
env:
  CLOUDFLARE_TOKEN: ${{ secrets.CLOUDFLARE_TOKEN }}
jobs:
  publish:
    name: Publish DNS config from main
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: OctoDNS Sync
        uses: cfunkhouser/octodns-sync-action@v0.0.15
        with:
          octodns_config_file: "config/to-cloudflare.yaml"
          doit: "true"
```

### Diffs as PR Comments

```yaml
name: cloudflare-dns-review
on:
  # Push changes to the correct DNS providers when changes to the YAML zone files
  # are pushed to the main branch.
  pull_request:
env:
  CLOUDFLARE_TOKEN: ${{ secrets.CLOUDFLARE_TOKEN }}
jobs:
  publish:
    name: Publish DNS config from main
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: OctoDNS Diff
        uses: cfunkhouser/octodns-sync-action@v0.0.15
        with:
          octodns_config_file: "config/to-cloudflare.yaml"
          post_pr_comment: "true"
```
