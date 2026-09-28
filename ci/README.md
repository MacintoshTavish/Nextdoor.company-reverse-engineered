# Optional GitHub Actions checks

The publishing OAuth token allows repository pushes but lacks GitHub workflow scope. GitHub rejected an attempt to publish an active workflow, so the configuration is retained as `github-actions.example.yml` and is not active. All documented checks passed locally before publication.

To enable it with suitable repository authorization, copy the example to `.github/workflows/checks.yml` and commit it. The example has read-only repository permissions, uses commit-pinned official actions, and runs only offline checks. It does not schedule collection or submit requests to the target.
