#!/usr/bin/env python3
"""Verify the local, self-contained inventory page in a fresh browser."""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

BASE = Path(__file__).resolve().parent


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 960})
        await context.route('http://**/*', lambda route: route.abort())
        await context.route('https://**/*', lambda route: route.abort())
        page = await context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        await page.goto((BASE / 'company-source-index.html').as_uri())
        assert await page.locator('tbody tr').count() == 460
        results = []
        for query, expected in [('Postman', 1), ('not-found', 6), ('unlikely-absent-needle-4671', 0), ('', 460)]:
            await page.locator('#search').fill(query)
            actual = await page.locator('tbody tr:not([hidden])').count()
            assert actual == expected, (query, actual, expected)
            results.append({'query': query, 'visible_rows': actual})
        assert not errors, errors
        await page.screenshot(path=str(BASE / 'inventory-browser-check.png'))
        (BASE / 'inventory-browser-check.json').write_text(json.dumps({'local_only': True,
            'external_requests': 'blocked', 'filter_checks': results, 'page_errors': errors}, indent=2) + '\n')
        await browser.close()
        print(json.dumps(results))


asyncio.run(main())
