# Offline frontend reproductions

Run with Node.js:

```sh
node frontend-repros/run.mjs
```

The script reads only `extracted-source.json` beside itself. It makes no requests, opens no browser or checkout, submits no forms, and uses only synthetic fixture data. `fetch` is always mocked; checkout URLs are printed without navigation. Source snippets are evaluated in isolated VM contexts with no supplied filesystem, network, application account, or real browser storage interfaces. This is an execution setup for these particular excerpts, not a general guarantee that Node's VM can sandbox arbitrary hostile code.

`extracted-source.json` retains exact function/module excerpts from the inspected public bundles, with the notification header value redacted. Each source path and SHA-256 identifies the local input used. The earlier listing bundle was already redacted before these tests, so its retained SHA-256 is not the hash of unredacted network bytes.

The assertions reproduce existing defects; passing means the observed behavior was reproduced. They are not production regression tests whose passing indicates a fix.

The markup check uses an inert `<b>` element in an owned in-memory fixture. It proves missing output escaping; it does not establish that an attacker can persist a field in the production ingest pipeline. The hostname test proves permissive frontend validation; it does not establish an unauthorized access grant.
