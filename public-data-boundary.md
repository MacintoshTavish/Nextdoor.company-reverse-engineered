# Public company data versus the login gate

Observed 28 September 2026. Public availability is confirmed; whether this violates the intended product boundary remains an owner decision.

The anonymous homepage loads a manifest of 460 company modules. Preview logic selects ten records, masks other markers and suppresses links in the client. Clicking a locked marker opens a Google/LinkedIn login prompt. The public module paths still contain detailed company data and original job/application links. The bounded audit fetched and parsed all 460 pinned modules successfully.

The normal `/api/discover-map-data` and `/api/company-leadership?id=105&slug=superk` endpoints returned 401 without login. This establishes a contrasting API gate, not private customer-record exposure or a demonstrated paid entitlement bypass.

## Reproduce with a minimal public example

1. Open the homepage without signing in and inspect the preview/login behavior.
2. Inspect the public loader [14401-24a4271828265f87.js](https://www.nextdoor.company/_next/static/chunks/14401-24a4271828265f87.js) and its referenced runtime from the pinned deployment.
3. Read [the SuperK module](https://www.nextdoor.company/_next/static/chunks/53769.6aff91071adeab42.js) without credentials. The audit observed HTTP 200, 14,839 bytes and 12 jobs. Its exact hash and sanitized fields are in [inventory/companies/superk.json](inventory/companies/superk.json).
4. Compare the protected APIs' anonymous rejection in [evidence/followup-api-responses.json](evidence/followup-api-responses.json).

The sample has public immutable cache headers with a one-year max-age. Frontend masking cannot retract the underlying original fields. Repeated previews can also select different companies, which further limits a confidentiality claim based only on the ten-record preview.

## Impact and triage

Anonymous access to the published company corpus is demonstrated. Registration/content-gating impact is plausible only if those fields were intended to require membership. No user sessions, private profiles, resumes, payment details, database write access or backend parity were established. Severity on demonstrated facts is informational/low or a product-design observation, depending on owner intent; a high-severity breach or bounty entitlement is unsupported.

If the full data is restricted, exclude it from public imports/static builds, publish an explicit preview schema and authorize complete responses server-side. Review previously published assets and caches; assume copies already downloaded cannot be recalled. If the full data is intended to be public, keep that policy explicit and protect user-specific records separately.

Preview screenshots and sanitized browser observations are included under `evidence/`. They were captured earlier in the same review; the company inventory was subsequently completed against the newer pinned manifest. No login, mutation, notification or external disclosure was performed.
