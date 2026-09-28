import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

// Only local, redacted source excerpts are read. All application I/O is mocked.
const evidence = JSON.parse(fs.readFileSync(new URL('./extracted-source.json', import.meta.url), 'utf8'));
const results = [];
const quiet = { log() {}, warn() {}, error() {} };
function context(globals = {}) {
  return vm.createContext({ console: quiet, URL, setTimeout, clearTimeout, ...globals });
}
function run(source, globals = {}) {
  return vm.runInContext(`(${source})`, context(globals), { timeout: 1000 });
}
function loader(globals = {}) {
  const scope = context(globals);
  const cache = {};
  function requireModule(id) {
    if (cache[id]) return cache[id].exports;
    if (!evidence.modules[id]) return id === 41413 ? { W8: () => '' } : {};
    const module = { exports: {} };
    cache[id] = module;
    const fn = vm.runInContext(`(${evidence.modules[id]})`, scope, { timeout: 1000 });
    fn(module, module.exports, requireModule);
    return module.exports;
  }
  requireModule.d = (out, definitions) => {
    for (const [key, get] of Object.entries(definitions)) Object.defineProperty(out, key, { get });
  };
  requireModule.hmd = module => module;
  requireModule.g = scope;
  return requireModule;
}

{
  const browserProcess = loader()(68867);
  const checkout = run(evidence.snippets.checkout, { x: browserProcess });
  const observed = { environment_keys: Object.keys(browserProcess.env), one_time_url: checkout('onetime'), growth_url: checkout('growth') };
  assert.equal(observed.one_time_url, 'https://checkout.dodopayments.com/buy/undefined?quantity=1');
  assert.equal(observed.growth_url, observed.one_time_url);
  results.push({ id: 'checkout-missing-product-id', observed, external_requests: 0 });
}

for (const failure of ['network-rejection', 'http-503']) {
  const events = [];
  const module = () => ({ default: { capture: name => events.push(['analytics', name]) } });
  const submit = run(evidence.snippets.freeCompany, {
    es: () => true, Z: () => '+15555550100', L: value => events.push(['loading', value]),
    j: 'Owned fixture', k: 'https://example.invalid', S: 'https://example.invalid/careers', C: 'audit@example.invalid',
    R: 'free', b: { free: { price: 0, type: '' } }, localStorage: { setItem() {} }, a: module,
    fetch: async () => {
      events.push(['mock-fetch', failure]);
      if (failure === 'network-rejection') throw Error('Simulated network failure');
      return { ok: false, status: 503 };
    },
    I: value => events.push(['success', value]), v: () => events.push(['onSubmitted', true]),
    alert: () => events.push(['alert', true]),
  });
  await submit();
  assert.ok(events.some(([name, value]) => name === 'success' && value));
  assert.ok(events.some(([name]) => name === 'onSubmitted'));
  results.push({ id: 'free-company-false-success', scenario: failure, observed: events, external_requests: 0 });
}

{
  let calls = 0;
  const api = loader({ fetch: async () => {
    calls += 1;
    return calls === 1 ? { ok: false, status: 503 } : { ok: true, json: async () => ({ founders: [{ name: 'Owned founder fixture' }] }) };
  } })(61639);
  const first = await api.zz('owned-fixture', 'owned-fixture');
  const second = await api.zz('owned-fixture', 'owned-fixture');
  assert.equal(first.length, 0);
  assert.equal(second.length, 0);
  assert.equal(calls, 1);
  results.push({ id: 'leadership-http-error-cached-as-empty', observed: { first, second, fetch_calls: calls }, external_requests: 0 });
}

for (const failure of ['http-500', 'network-rejection', 'http-200-control']) {
  const events = [];
  const parent = run(evidence.snippets.signupParent, {
    fetch: async () => {
      events.push(['mock-fetch', failure]);
      if (failure === 'network-rejection') throw Error('Simulated network failure');
      return { ok: failure === 'http-200-control', status: failure === 'http-200-control' ? 200 : 500 };
    },
    i: { default: { capture: name => events.push(['parent-analytics', name]) } },
    y: value => events.push(['modal-open', value]),
  });
  const child = run(evidence.snippets.signupChild, {
    g: 'Owned fixture', b: 'audit@example.invalid', f: 'https://www.linkedin.com/in/owned-fixture', S: 'engineering',
    u: null, M: () => true, P: () => true, B() {}, x() {}, p: parent,
    e: () => ({ default: { capture: name => events.push(['child-analytics', name]) } }),
    N: value => events.push(['success', value]), A() {}, C() {}, E() {}, y() {}, w() {}, v() {}, j() {},
    alert: () => events.push(['alert', true]),
  });
  await child();
  assert.ok(events.some(([name, value]) => name === 'success' && value));
  results.push({ id: 'job-alert-false-success', scenario: failure, observed: events, external_requests: 0 });
}

{
  const render = loader({ window: {} })(16400).r;
  const marker = '<b data-audit-marker="local-only">owned fixture</b>';
  const fixture = {
    id: 1, company_basic_information: { logo_url: '', company_name_brand: marker, careers_url: 'https://example.invalid/careers' },
    financial_information: {}, business_details: { description: marker }, leadership: { founders: [] },
    location_mapping: [], social_media: {}, job_data: { roles: [], total_roles: 0 }, current_status: {}, benefits: {},
  };
  const html = render({ company: fixture, filters: {}, isSidebar: true });
  const observed = { raw_inert_markup_count: html.split(marker).length - 1, escaped_marker_found: html.includes('&lt;b data-audit-marker') };
  assert.equal(observed.raw_inert_markup_count, 2);
  assert.equal(observed.escaped_marker_found, false);
  results.push({ id: 'raw-html-interpolation', observed, external_requests: 0, limitation: 'Inert markup only. No script executed and no persisted attacker-controlled source path demonstrated.' });
}

{
  const platform = run(evidence.snippets.freeAccessPlatform);
  const video = run(evidence.snippets.freeAccessVideo);
  const urls = ['https://www.instagram.com/reel/owned-fixture/', 'https://instagram.com.example.invalid/reel/owned-fixture/', 'https://tiktok.com.example.invalid/@owned/video/123'];
  const observed = urls.map(url => ({ url, platform: platform(url), accepted_as_video: video(url) }));
  assert.ok(observed.every(row => row.accepted_as_video));
  results.push({ id: 'free-access-lookalike-host-validation', observed, external_requests: 0, limitation: 'Client validation only; no access grant or server acceptance tested.' });
}

{
  const render = loader({ window: {} })(16400).r;
  const fixture = {
    id: 1, company_basic_information: { logo_url: '', company_name_brand: 'Owned fixture', careers_url: 'https://example.invalid/careers' },
    financial_information: {}, business_details: { description: 'Owned test record' }, leadership: { founders: [] },
    location_mapping: [], social_media: {}, job_data: { roles: [], total_roles: 0, crawl_status: 'failed' }, current_status: {}, benefits: {},
  };
  const html = render({ company: fixture, filters: {}, isSidebar: true });
  const observed = { failed_crawl_labelled_not_hiring: html.includes('>NOT HIRING</div>'), crawl_failure_explained: html.includes('crawl_status') || html.includes('crawl failed') };
  assert.equal(observed.failed_crawl_labelled_not_hiring, true);
  results.push({ id: 'zero-role-failed-crawl-hiring-label', observed, external_requests: 0, limitation: 'Owned fixture proves renderer behavior; whether ingest publishes failed crawls as zero roles is a separate data-pipeline question.' });
}

{
  const render = loader({ window: {} })(16400).r;
  const fixture = {
    id: 1, company_basic_information: { logo_url: '', company_name_brand: 'Owned fixture', careers_url: 'https://example.invalid/careers' },
    financial_information: {}, business_details: { description: 'Owned test record' }, leadership: { founders: [] }, social_media: {}, current_status: {}, benefits: {},
    location_mapping: [
      { location_id: 'queensland_office', city: 'Brisbane', state: 'Queensland', country: 'Australia', exact_address: 'Brisbane,Queensland,Australia', location_source: 'state_capital_representative' },
      { location_id: 'melbourne_office', city: 'Melbourne', country: 'Australia', exact_address: 'Melbourne,Australia', location_source: 'city_representative' },
    ],
    job_data: { total_roles: 1, roles: [{ title: 'Owned fixture role', apply_url: 'https://example.invalid/job', work_mode: 'on-site', location_ids: ['melbourne_office', 'queensland_office'], location_display: 'Melbourne,Australia / Queensland,Australia' }] },
  };
  const html = render({ company: fixture, filters: {}, isSidebar: true, clickedLocationId: 'queensland_office' });
  const observed = {
    office_address_label: html.includes('>Office address:</span>'),
    representative_address_displayed: html.includes('Brisbane,Queensland,Australia'),
    office_network_label: html.includes('Office network (i.e. hiring in 2 locations)'),
    representative_provenance_displayed: html.includes('state_capital_representative'),
  };
  assert.equal(observed.office_address_label, true);
  assert.equal(observed.representative_address_displayed, true);
  assert.equal(observed.office_network_label, true);
  assert.equal(observed.representative_provenance_displayed, false);
  results.push({ id: 'representative-geocode-rendered-as-office', observed, external_requests: 0, fixture_provenance: 'Synthetic company/role with public Databricks location shape from inventory/companies/databricks.json; no claimed physical office verification.' });
}

console.log(JSON.stringify({ date: evidence.date, mode: 'offline-only', results }, null, 2));
