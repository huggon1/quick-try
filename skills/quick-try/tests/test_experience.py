"""Offline behavior and hostile-input checks for the portable experience bundle."""

import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))
import experience  # noqa: E402


def sample_data():
    """A valid authored bundle, independent of the generated draft defaults."""
    return {
        "schema_version": 1,
        "id": "offline-example",
        "title": "Offline example",
        "language": "en",
        "kind": "model",
        "mode": "self",
        "status": "ready",
        "summary": "A deterministic fixture, not a real model evaluation.",
        "goal": "Inspect a saved output and its original input.",
        "target": {"name": "Example", "url": "https://example.com/", "version": "fixture-1"},
        "budget": {"preparation": "No execution", "hands_on": "One minute", "cost": "None"},
        "authorization": {"scope": "Read fixture files.", "constraints": ["Do not call any service."]},
        "requirements": [{"name": "Sample", "status": "available", "detail": "Saved locally."}],
        "capabilities": [],
        "entry": {"label": "View the sample", "url": "artifacts/result.txt"},
        "baseline": "Start with the saved input.",
        "reset": "Reopen the unchanged fixture.",
        "steps": [{"id": "inspect", "title": "Inspect the sample", "instruction": "Read the local result.",
                   "input": "An example input.", "expected": "Observe whether it preserves the input.",
                   "variations": ["Change the input in a future run."]}],
        "sources": [{"id": "example-docs", "title": "Example source", "url": "https://example.com/docs",
                     "kind": "first-party", "accessed": "2026-09-08", "context": "Fixture metadata."}],
        "artifacts": [{"id": "result", "path": "artifacts/result.txt", "label": "Saved result", "kind": "file"}],
        "observations": [{"id": "inspected", "actor": "user", "method": "manual", "step_id": "inspect",
                          "action": "Opened the sample.", "input": "The saved input.",
                          "observed": "The fixture file contains the sample text.", "outcome": "success",
                          "artifact_ids": ["result"], "recorded_at": "2026-09-08T10:00:00+08:00",
                          "settings": "Offline fixture; no model call."}],
        "verification": [{"check": check, "status": "passed", "observation_ids": ["inspected"],
                          "detail": "Manually verified the fixture."}
                         for check in ("entry", "sample", "core-action", "reset")],
        "limitations": ["This is a test fixture, not evidence about a product."],
        "next_steps": ["Replace this fixture with actual experience data."],
        "notes": [{"id": "note-original", "created_at": "2026-09-08T02:00:00Z",
                   "text": "An existing note must survive an import."}],
    }


class BundleCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "bundle"
        self.root.mkdir()
        (self.root / "artifacts").mkdir()
        (self.root / "artifacts/result.txt").write_text("Sample output.\n", encoding="utf-8")
        self.data = sample_data()

    def save(self, data=None):
        path = self.root / "experience.json"
        path.write_text(json.dumps(self.data if data is None else data, ensure_ascii=False), encoding="utf-8")
        return path

    def reject(self, data):
        with self.assertRaises(ValueError):
            experience.validate(data, self.root)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "experience.py"), *map(str, args)],
                              cwd=self.base, capture_output=True, text=True, timeout=10)


class ValidationTests(BundleCase):
    def test_valid_bundle_and_draft_are_accepted_without_execution(self):
        self.assertIs(experience.validate(self.data, self.root), self.data)
        draft = copy.deepcopy(self.data)
        draft.update(status="draft", entry=None, artifacts=[], observations=[], verification=[])
        draft["requirements"][0]["status"] = "unknown"
        self.assertIs(experience.validate(draft, self.root), draft)
        draft["status"] = "ready"
        self.reject(draft)

    def test_each_ready_requirement_is_required(self):
        mutations = {
            "missing entry": lambda d: d.update(entry=None),
            "missing resource": lambda d: d["requirements"][0].update(status="missing"),
            "unknown resource": lambda d: d["requirements"][0].update(status="unknown"),
            "missing check": lambda d: d["verification"].pop(),
            "unverified check": lambda d: d["verification"][0].update(status="unverified"),
            "failed check": lambda d: d["verification"][0].update(status="failed"),
            "no observation": lambda d: d["verification"][0].update(observation_ids=[]),
            "no saved evidence": lambda d: d["observations"][0].update(artifact_ids=[]),
            "failed observation": lambda d: d["observations"][0].update(outcome="failure"),
            "partial observation": lambda d: d["observations"][0].update(outcome="partial"),
            "empty steps": lambda d: d.update(steps=[]),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                data = copy.deepcopy(self.data)
                mutate(data)
                self.reject(data)

    def test_ready_agent_demo_requires_actual_agent_observation_and_capability(self):
        self.data["mode"] = "agent-demo"
        self.reject(self.data)
        observation = self.data["observations"][0]
        observation.update(actor="agent", method="browser")
        for status in (None, "unknown", "unavailable"):
            with self.subTest(status=status):
                self.data["capabilities"] = [] if status is None else [
                    {"name": "browser", "status": status, "detail": "Fixture capability."}]
                self.reject(self.data)
        self.data["capabilities"][0]["status"] = "available"
        experience.validate(self.data, self.root)

    def test_observation_methods_match_actor_and_available_capability(self):
        for method in ("cli", "api", "browser", "desktop"):
            with self.subTest(method=method):
                data = copy.deepcopy(self.data)
                data["observations"][0].update(actor="agent", method=method)
                self.reject(data)
                data["capabilities"] = [{"name": method, "status": "available", "detail": "Fixture only."}]
                experience.validate(data, self.root)
                data["observations"][0]["actor"] = "user"
                self.reject(data)
        self.data["observations"][0]["actor"] = "agent"
        self.reject(self.data)

    def test_ready_demo_covers_each_planned_step_with_agent_evidence(self):
        self.data["mode"] = "agent-demo"
        self.data["capabilities"] = [{"name": "cli", "status": "available", "detail": "Offline fixture."}]
        self.data["observations"][0].update(actor="agent", method="cli")
        second_step = copy.deepcopy(self.data["steps"][0])
        second_step.update(id="second-action", title="Inspect another condition")
        self.data["steps"].append(second_step)
        self.reject(self.data)
        second_observation = copy.deepcopy(self.data["observations"][0])
        second_observation.update(id="second-inspection", step_id="second-action")
        self.data["observations"].append(second_observation)
        experience.validate(self.data, self.root)
        second_observation["artifact_ids"] = []
        self.reject(self.data)
        second_observation.update(artifact_ids=["result"], actor="user", method="manual")
        self.reject(self.data)

    def test_broken_references_are_rejected_even_in_drafts(self):
        mutations = (
            lambda d: d["observations"][0].update(step_id="missing-step"),
            lambda d: d["observations"][0].update(artifact_ids=["missing-artifact"]),
            lambda d: d["verification"][0].update(observation_ids=["missing-observation"]),
            lambda d: d["observations"][0].update(artifact_ids=["result", "result"]),
            lambda d: d["verification"][0].update(observation_ids=["inspected", "inspected"]),
        )
        for index, mutate in enumerate(mutations):
            with self.subTest(case=index):
                data = copy.deepcopy(self.data)
                data["status"] = "draft"
                mutate(data)
                self.reject(data)

    def test_duplicate_ids_names_and_checks_are_rejected(self):
        for collection in ("steps", "sources", "artifacts", "observations", "notes", "requirements", "verification"):
            with self.subTest(collection=collection):
                data = copy.deepcopy(self.data)
                data[collection].append(copy.deepcopy(data[collection][0]))
                self.reject(data)
        self.data["capabilities"] = [{"name": "cli", "status": "available", "detail": "Fixture only."}] * 2
        self.reject(self.data)

    def test_artifact_path_traversal_and_reserved_names_are_rejected(self):
        paths = ("../outside.txt", "/tmp/outside.txt", "artifacts/../experience.json",
                 "artifacts//result.txt", "artifacts/./result.txt", "artifacts\\result.txt",
                 "artifacts/result.txt?download=1", "artifacts/result.txt#part", "artifacts/result.txt\n",
                 "artifacts/missing.txt")
        for path in paths:
            with self.subTest(path=path):
                data = copy.deepcopy(self.data)
                data["artifacts"][0]["path"] = path
                self.reject(data)

    def test_artifact_file_and_directory_symlinks_are_rejected(self):
        outside = self.base / "outside.txt"
        outside.write_text("Private data", encoding="utf-8")
        link = self.root / "artifacts/link.txt"
        link.symlink_to(outside)
        self.data["artifacts"][0]["path"] = "artifacts/link.txt"
        self.reject(self.data)
        (self.root / "artifacts/linked-dir").symlink_to(self.base, target_is_directory=True)
        self.data["artifacts"][0]["path"] = "artifacts/linked-dir/outside.txt"
        self.reject(self.data)
        link.unlink()
        link.symlink_to(self.root / "artifacts/result.txt")
        self.data["artifacts"][0]["path"] = "artifacts/link.txt"
        self.reject(self.data)

    def test_bundle_root_symlink_is_rejected(self):
        alias = self.base / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            experience.validate(self.data, alias)

    def test_missing_evidence_and_disguised_images_are_rejected(self):
        (self.root / "artifacts/result.txt").unlink()
        self.reject(self.data)
        for suffix, content in ((".svg", b'<svg xmlns="http://www.w3.org/2000/svg"/>'),
                                (".png", b'<html><script>alert(1)</script></html>'),
                                (".jpg", b"GIF89a fake jpeg")):
            with self.subTest(suffix=suffix):
                path = "artifacts/picture" + suffix
                (self.root / path).write_bytes(content)
                self.data["artifacts"][0].update(path=path, kind="image")
                self.reject(self.data)

    def test_url_schemes_credentials_and_ambiguous_hosts_are_rejected(self):
        urls = ("javascript:alert(1)", "data:text/html,test", "file:///etc/passwd", "ftp://example.com/x",
                "http://example.com/", "https://name:secret@example.com/", "https://name@example.com/",
                "https://", "//example.com/", "https://example.com\\@localhost/", "https://exa mple.com/",
                "https://example.com/\n", "https://example.com:99999/", "https://[::1")
        for field in ("target", "entry"):
            for value in urls:
                with self.subTest(field=field, value=value):
                    data = copy.deepcopy(self.data)
                    data[field]["url"] = value
                    self.reject(data)

    def test_https_and_explicit_loopback_urls_are_supported(self):
        for value in ("https://example.com/a?q=1#result", "http://localhost:8123/",
                      "http://127.0.0.1:8123/", "http://[::1]:8123/"):
            with self.subTest(value=value):
                self.data["entry"]["url"] = value
                experience.validate(self.data, self.root)

    def test_target_can_reference_an_existing_local_project(self):
        demo = self.root / "artifacts/demo.html"
        demo.write_text("<!doctype html><title>Local project</title><p>Prepared example.</p>", encoding="utf-8")
        self.data["target"].update(name="Local project", url="artifacts/demo.html", version="local-fixture-1")
        self.data["entry"]["url"] = "artifacts/demo.html"
        experience.validate(self.data, self.root)
        self.save()
        result = self.cli("validate", self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        demo.unlink()
        self.reject(self.data)

    def test_timestamp_needs_timezone_and_schema_cannot_be_boolean(self):
        for stamp in ("2026-09-08T10:00:00", "not-a-date", "2026-09-08T10:00:00+99:00"):
            with self.subTest(stamp=stamp):
                data = copy.deepcopy(self.data)
                data["observations"][0]["recorded_at"] = stamp
                self.reject(data)
        self.data["schema_version"] = True
        self.reject(self.data)

    def test_nontext_step_reference_is_rejected_without_traceback(self):
        for step_id in ([], {}, None, 42):
            with self.subTest(step_id=step_id):
                data = copy.deepcopy(self.data)
                data["observations"][0]["step_id"] = step_id
                self.reject(data)
                self.save(data)
                result = self.cli("validate", self.root)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)

    def test_source_access_date_uses_documented_calendar_format(self):
        for stamp in ("20260908", "2026-W37-2", "2026-09-08T00:00:00Z"):
            with self.subTest(stamp=stamp):
                data = copy.deepcopy(self.data)
                data["sources"][0]["accessed"] = stamp
                self.reject(data)

    def test_json_duplicate_keys_and_nonfinite_numbers_are_rejected(self):
        for content in ('{"id":"first","id":"second"}', '{"outer":{"x":1,"x":2}}',
                        '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}'):
            with self.subTest(content=content):
                path = self.base / "invalid.json"
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    experience.load_json(path)

    def test_json_symlink_and_oversized_input_are_rejected(self):
        source = self.save()
        alias = self.base / "alias.json"
        alias.symlink_to(source)
        with self.assertRaises(ValueError):
            experience.load_json(alias)
        big = self.base / "big.json"
        with big.open("wb") as handle:
            handle.truncate(experience.MAX_JSON + 1)
        with self.assertRaises(ValueError):
            experience.load_json(big)

    def test_cli_validation_error_preserves_source(self):
        self.data["requirements"][0]["status"] = "unknown"
        source = self.save()
        before = source.read_bytes()
        result = self.cli("validate", self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(source.read_bytes(), before)


class CommandTests(BundleCase):
    def test_new_creates_only_a_draft_and_never_overwrites(self):
        destination = self.base / "new-experience"
        result = self.cli("new", destination, "--title", "Example", "--kind", "product",
                          "--target-url", "https://example.com/", "--language", "zh-CN")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = experience.load_json(destination / "experience.json")
        self.assertEqual(data["status"], "draft")
        self.assertIsNone(data["entry"])
        self.assertEqual(data["observations"], [])
        self.assertEqual(data["verification"], [])
        self.assertTrue((destination / "index.html").is_file())
        before = {path.name: path.read_bytes() for path in destination.iterdir() if path.is_file()}
        second = self.cli("new", destination, "--title", "Replacement", "--kind", "model",
                          "--target-url", "https://example.com/")
        self.assertNotEqual(second.returncode, 0)
        self.assertEqual(before, {path.name: path.read_bytes() for path in destination.iterdir() if path.is_file()})

    def test_invalid_new_leaves_no_bundle_or_staging_directory(self):
        destination = self.base / "invalid-new"
        result = self.cli("new", destination, "--title", "Example", "--kind", "model",
                          "--target-url", "javascript:alert(1)")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(destination.exists())
        self.assertEqual(list(self.base.glob(".experience-*")), [])

    def test_render_preserves_canonical_data_and_rejects_output_symlink(self):
        source = self.save()
        before = source.read_bytes()
        result = self.cli("render", self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(source.read_bytes(), before)
        target = self.base / "must-not-change.html"
        target.write_text("Protected", encoding="utf-8")
        (self.root / "index.html").unlink()
        (self.root / "index.html").symlink_to(target)
        result = self.cli("render", self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target.read_text(encoding="utf-8"), "Protected")
        self.assertEqual(source.read_bytes(), before)

    def note_file(self, *, identity=None, note_id="note-imported", text="A new observation."):
        path = self.base / "notes.json"
        path.write_text(json.dumps({"schema_version": 1, "experience_id": identity or self.data["id"],
                                    "note": {"id": note_id, "created_at": "2026-09-08T03:00:00Z", "text": text}}),
                        encoding="utf-8")
        return path

    def test_notes_append_preserve_content_and_are_idempotent(self):
        source = self.save()
        initial = copy.deepcopy(self.data)
        notes_path = self.note_file(text="中文 note with <markup> and a newline.\nSecond line.")
        result = self.cli("import-notes", self.root, notes_path)
        self.assertEqual(result.returncode, 0, result.stderr)
        after = experience.load_json(source)
        self.assertEqual(after["notes"][:-1], initial["notes"])
        self.assertEqual({k: v for k, v in after.items() if k != "notes"},
                         {k: v for k, v in initial.items() if k != "notes"})
        self.assertEqual(after["notes"][-1]["text"], "中文 note with <markup> and a newline.\nSecond line.")
        source_before = source.read_bytes()
        page_before = (self.root / "index.html").read_bytes()
        result = self.cli("import-notes", self.root, notes_path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(source.read_bytes(), source_before)
        self.assertEqual((self.root / "index.html").read_bytes(), page_before)

    def test_notes_wrong_experience_and_id_conflict_preserve_both_files(self):
        source = self.save()
        self.assertEqual(self.cli("render", self.root).returncode, 0)
        for note_args in ({"identity": "somebody-else"}, {"note_id": "note-original", "text": "Conflicting text"}):
            with self.subTest(note_args=note_args):
                notes_path = self.note_file(**note_args)
                tracked = (source, self.root / "index.html", notes_path)
                before = {str(path): path.read_bytes() for path in tracked}
                result = self.cli("import-notes", self.root, notes_path)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(before, {str(path): path.read_bytes() for path in tracked})

    def test_notes_failed_page_write_preserves_canonical_bundle(self):
        source = self.save()
        before = source.read_bytes()
        (self.root / "index.html").mkdir()
        notes_path = self.note_file()
        result = self.cli("import-notes", self.root, notes_path)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(source.read_bytes(), before,
                         "A rejected import must not leave a canonical note committed with no updated page.")

    def test_notes_exceeding_canonical_byte_limit_preserve_source_and_page(self):
        self.data["limitations"] = []
        target_size = experience.MAX_JSON - 8192
        while True:
            serialized_size = len((json.dumps(self.data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
            room = target_size - serialized_size - 12
            if room <= 0:
                break
            self.data["limitations"].append("x" * min(19000, room))
        source = self.save()
        self.assertLess(source.stat().st_size, experience.MAX_JSON)
        experience.validate(experience.load_json(source), self.root)
        rendered = self.cli("render", self.root)
        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        notes_path = self.note_file(text="é" * 20000)
        envelope = experience.load_json(notes_path)
        proposed = copy.deepcopy(self.data)
        proposed["notes"].append(envelope["note"])
        proposed_bytes = (json.dumps(proposed, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        self.assertGreater(len(proposed_bytes), experience.MAX_JSON)
        tracked = (source, self.root / "index.html", notes_path)
        before = {path: path.read_bytes() for path in tracked}
        result = self.cli("import-notes", self.root, notes_path)
        self.assertNotEqual(result.returncode, 0,
                            "Import must reject output that a future load_json cannot read.")
        self.assertEqual(before, {path: path.read_bytes() for path in tracked})
        experience.validate(experience.load_json(source), self.root)


class ParsedPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class RendererTests(BundleCase):
    def render(self):
        from render_page import render_page
        experience.validate(self.data, self.root)
        rendered = render_page(self.data)
        parsed = ParsedPage()
        parsed.feed(rendered)
        return rendered, parsed

    def test_content_is_literal_text_and_not_executable_markup(self):
        payload = '<img src=x onerror="alert(1)"><script>alert("injected")</script> & "quoted"'
        self.data["title"] = payload
        self.data["goal"] = payload
        self.data["steps"][0]["instruction"] = payload
        self.data["observations"][0]["observed"] = payload
        self.data["notes"][0]["text"] = payload
        self.data["entry"]["label"] = payload
        rendered, parsed = self.render()
        self.assertNotIn(payload, rendered)
        self.assertIn(payload, "".join(parsed.text))
        self.assertFalse(any("onerror" in attrs for _, attrs in parsed.tags))
        self.assertFalse(any(tag == "img" and attrs.get("src") == "x" for tag, attrs in parsed.tags))
        self.assertNotIn('<script>alert("injected")</script>', rendered)

    def test_local_paths_are_quoted_and_target_html_is_not_inlined(self):
        name = 'artifacts/demo "quoted" <page>.html'
        (self.root / name).write_text('<html><script>window.INLINE_SENTINEL = 1</script></html>', encoding="utf-8")
        self.data["entry"]["url"] = name
        self.data["artifacts"].append({"id": "local-demo", "path": name, "label": "Open demo", "kind": "file"})
        rendered, parsed = self.render()
        self.assertNotIn("INLINE_SENTINEL", rendered)
        hrefs = [attrs.get("href", "") for _, attrs in parsed.tags]
        self.assertTrue(any("%22quoted%22" in href and "%3Cpage%3E" in href for href in hrefs), hrefs)
        self.assertFalse(any(tag in {"iframe", "object", "embed"} for tag, _ in parsed.tags))

    def test_page_has_no_remote_assets_or_executable_data_interpolation(self):
        self.data["summary"] = '</script><script>window.SUMMARY_SENTINEL = true;</script>'
        rendered, parsed = self.render()
        for tag, attrs in parsed.tags:
            if tag in {"script", "img", "link", "iframe", "audio", "video", "source"}:
                url = attrs.get("src", attrs.get("href", ""))
                self.assertFalse(url.startswith(("https:", "http:", "//")), (tag, url))
        self.assertNotIn('</script><script>window.SUMMARY_SENTINEL', rendered)

    def test_nonready_entries_remain_references_in_both_locales(self):
        labels = {"en": ("Open reference only", "Open the experience"),
                  "zh-CN": ("仅打开参考入口", "打开体验")}
        for status in ("draft", "blocked"):
            for language, (reference, start) in labels.items():
                with self.subTest(status=status, language=language):
                    self.data.update(status=status, language=language)
                    self.data["verification"] = []
                    _, parsed = self.render()
                    readable = "".join(parsed.text)
                    self.assertIn(reference, readable)
                    self.assertNotIn(start, readable)

    def test_semantic_content_survives_without_javascript_for_all_kinds_and_locales(self):
        for kind in ("model", "harness", "product", "prompt"):
            for language in ("en", "zh-CN"):
                with self.subTest(kind=kind, language=language):
                    self.data.update(kind=kind, language=language)
                    _, parsed = self.render()
                    readable = "".join(parsed.text)
                    for expected in (self.data["goal"], self.data["reset"], self.data["steps"][0]["instruction"],
                                     self.data["steps"][0]["expected"], self.data["observations"][0]["observed"],
                                     self.data["notes"][0]["text"]):
                        self.assertIn(expected, readable)
                    html = next(attrs for tag, attrs in parsed.tags if tag == "html")
                    self.assertEqual(html.get("lang"), language)
                    body = next(attrs for tag, attrs in parsed.tags if tag == "body")
                    self.assertEqual(body.get("data-experience-id"), self.data["id"])
                    self.assertTrue(any(tag == "h1" for tag, _ in parsed.tags))
                    self.assertTrue(any(tag == "textarea" and attrs.get("id") == "note-text" for tag, attrs in parsed.tags))
                    self.assertFalse(any("hidden" in attrs for _, attrs in parsed.tags
                                         if "data-panel" in attrs or "step-card" in attrs.get("class", "").split()),
                                     "Authored content must be visible before JavaScript enhances the page.")


if __name__ == "__main__":
    unittest.main()
