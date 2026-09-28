import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import monitor


class MonitorChecks(unittest.TestCase):
    def test_failure_keeps_existing_snapshot(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            old = {"companies": [{"slug": f"company-{i}", "name": None} for i in range(100)]}
            monitor.write_json(path / "latest.json", old)
            before = (path / "latest.json").read_bytes()
            with patch.object(monitor, "get", return_value=(200, "<html>Login required</html>", None)):
                with self.assertRaises(ValueError):
                    monitor.run(path)
            self.assertEqual(before, (path / "latest.json").read_bytes())

    def test_not_modified_preserves_companies_without_false_additions(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            companies = [{"slug": f"company-{i}", "name": f"Company {i}"} for i in range(100)]
            monitor.write_json(path / "latest.json", {"companies": companies, "source_assets": [],
                                                      "homepage_etag": '"test"'})
            with patch.object(monitor, "get", return_value=(304, "", None)) as fetch:
                monitor.run(path)
            latest = json.loads((path / "latest.json").read_text())
            self.assertEqual(companies, latest["companies"])
            self.assertEqual({"added": [], "removed": [], "renamed": []}, latest["changes"])
            fetch.assert_called_once()

    def test_changes_distinguish_new_company_from_new_name(self):
        before = [{"slug": "a", "name": "Old"}, {"slug": "b", "name": None},
                  {"slug": "removed", "name": "Gone"}]
        after = [{"slug": "a", "name": "New"}, {"slug": "b", "name": "Now Known"},
                 {"slug": "added", "name": "Added"}]
        changes = monitor.compare(before, after)
        self.assertEqual(["added"], [x["slug"] for x in changes["added"]])
        self.assertEqual(["removed"], [x["slug"] for x in changes["removed"]])
        self.assertEqual(["a"], [x["slug"] for x in changes["renamed"]])

    def test_large_drop_requires_review(self):
        with self.assertRaises(ValueError):
            monitor.validate_catalog([{}] * 460, [{"slug": str(i)} for i in range(100)])

    def test_does_not_follow_external_script_urls(self):
        parser = monitor.Scripts()
        parser.feed('<script src="https://elsewhere.invalid/_next/static/chunks/a.js"></script>'
                    '<script src="/_next/static/chunks/123-abcd.js?dpl=example"></script>')
        self.assertEqual([monitor.ORIGIN + "/_next/static/chunks/123-abcd.js"], parser.urls)


if __name__ == "__main__":
    unittest.main()
