#!/usr/bin/env python3
"""Create, validate and render private, portable experience bundles. Python 3.10+."""

import argparse
import datetime as dt
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile
from urllib.parse import urlsplit

MAX_JSON = 2 * 1024 * 1024
MAX_ARTIFACT = 32 * 1024 * 1024
KINDS = {"model", "harness", "product", "prompt"}
CHECKS = {"entry", "sample", "core-action", "reset"}


class Invalid(ValueError):
    """An actionable authoring or filesystem error."""


def require(condition, message):
    if not condition:
        raise Invalid(message)


def obj(value, fields, where):
    require(type(value) is dict, f"{where}: expected an object")
    require(set(value) == set(fields.split()),
            f"{where}: fields must be exactly {fields}")


def text(value, where, empty=False):
    require(type(value) is str and len(value) <= 20000, f"{where}: expected text up to 20000 characters")
    require(empty or bool(value.strip()), f"{where}: text is empty")
    require(not any(ord(c) < 32 and c not in "\n\r\t" for c in value), f"{where}: control character")


def choice(value, values, where):
    require(type(value) is str and value in values, f"{where}: expected one of {', '.join(sorted(values))}")


def seq(value, where):
    require(type(value) is list and len(value) <= 200, f"{where}: expected a list of at most 200 items")
    return value


def texts(value, where):
    for item in seq(value, where):
        text(item, where)


def slug(value, where):
    require(type(value) is str and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", value), f"{where}: use a lowercase slug")


def instant(value, where):
    text(value, where)
    try:
        stamp = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        require(stamp.tzinfo is not None, f"{where}: include a timezone")
    except ValueError as exc:
        raise Invalid(f"{where}: expected an ISO 8601 timestamp with timezone") from exc


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), f"not a regular non-symlink file: {path}")
    require(path.stat().st_size <= MAX_JSON, f"JSON exceeds {MAX_JSON} bytes: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates,
                          parse_constant=lambda v: (_ for _ in ()).throw(Invalid(f"invalid JSON number: {v}")))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise Invalid(f"cannot read JSON {path}: {exc}") from exc


def artifact_path(root, value):
    text(value, "artifact path")
    require(not any(c in value for c in "\\\r\n\t?#"), "artifact path contains a reserved character")
    path = PurePosixPath(value)
    require(not path.is_absolute() and path.parts and path.parts[0] == "artifacts"
            and len(path.parts) > 1 and ".." not in path.parts and str(path) == value,
            "local files must use normalized bundle-relative artifacts/... paths")
    current = root
    for part in path.parts:
        current = current / part
        require(not current.is_symlink(), f"symlinks are not portable evidence: {value}")
    require(current.is_file(), f"missing artifact: {value}")
    require(current.stat().st_size <= MAX_ARTIFACT, f"artifact exceeds {MAX_ARTIFACT} bytes: {value}")
    require(current.resolve().is_relative_to(root.resolve()), f"artifact escapes bundle: {value}")
    return current


def url(value, where, root=None):
    text(value, where)
    require(not any(ord(c) < 32 for c in value) and "\\" not in value, f"{where}: unsafe URL characters")
    parsed = urlsplit(value)
    if not parsed.scheme and root is not None:
        return artifact_path(root, value)
    require(not any(c.isspace() for c in value), f"{where}: URL contains whitespace")
    require(parsed.scheme in {"https", "http"} and bool(parsed.hostname), f"{where}: use HTTPS or explicit loopback HTTP")
    require(parsed.username is None and parsed.password is None, f"{where}: credentials do not belong in URLs")
    require(parsed.scheme == "https" or parsed.hostname in {"localhost", "127.0.0.1", "::1"},
            f"{where}: HTTP is limited to localhost, 127.0.0.1 or ::1")
    try:
        parsed.port
    except ValueError as exc:
        raise Invalid(f"{where}: invalid port") from exc


def keyed(items, fields, where):
    result = {}
    for item in seq(items, where):
        obj(item, fields, where)
        slug(item["id"], f"{where}.id")
        require(item["id"] not in result, f"{where}: duplicate id {item['id']}")
        result[item["id"]] = item
    return result


def references(values, known, where):
    texts(values, where)
    require(len(set(values)) == len(values), f"{where}: duplicate reference")
    for value in values:
        require(value in known, f"{where}: unknown reference {value}")


def validate(data, root):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), "bundle must be a real directory")
    obj(data, "schema_version id title language kind mode status summary goal target budget authorization requirements capabilities entry baseline reset steps sources artifacts observations verification limitations next_steps notes", "experience")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "unsupported schema_version")
    slug(data["id"], "experience.id")
    choice(data["kind"], KINDS, "kind")
    choice(data["mode"], {"self", "agent-demo"}, "mode")
    choice(data["status"], {"draft", "blocked", "ready"}, "status")
    choice(data["language"], {"en", "zh-CN"}, "language")
    for key in ("title", "summary", "goal", "baseline", "reset"):
        text(data[key], key)
    obj(data["target"], "name url version", "target")
    for key in ("name", "version"):
        text(data["target"][key], f"target.{key}")
    url(data["target"]["url"], "target.url", root)
    obj(data["budget"], "preparation hands_on cost", "budget")
    for key, value in data["budget"].items():
        text(value, f"budget.{key}")
    obj(data["authorization"], "scope constraints", "authorization")
    text(data["authorization"]["scope"], "authorization.scope")
    texts(data["authorization"]["constraints"], "authorization.constraints")
    capabilities = {}
    for collection in ("requirements", "capabilities"):
        names = set()
        for item in seq(data[collection], collection):
            obj(item, "name status detail", collection)
            text(item["name"], f"{collection}.name")
            require(item["name"] not in names, f"{collection}: duplicate name")
            names.add(item["name"])
            allowed = {"available", "missing", "unknown"} if collection == "requirements" else {"available", "unavailable", "unknown"}
            choice(item["status"], allowed, f"{collection}.status")
            text(item["detail"], f"{collection}.detail")
            if collection == "capabilities":
                capabilities[item["name"]] = item["status"]
    if data["entry"] is not None:
        obj(data["entry"], "label url", "entry")
        text(data["entry"]["label"], "entry.label")
        url(data["entry"]["url"], "entry.url", root)
    steps = keyed(data["steps"], "id title instruction input expected variations", "steps")
    require(bool(steps), "provide at least one concrete step")
    for item in steps.values():
        for key in ("title", "instruction", "input", "expected"):
            text(item[key], f"step.{key}")
        texts(item["variations"], "step.variations")
    sources = keyed(data["sources"], "id title url kind accessed context", "sources")
    for item in sources.values():
        for key in ("title", "context"):
            text(item[key], f"source.{key}")
        url(item["url"], "source.url")
        choice(item["kind"], {"first-party", "community"}, "source.kind")
        require(type(item["accessed"]) is str and re.fullmatch(r"\d{4}-\d{2}-\d{2}", item["accessed"]),
                "source.accessed: expected YYYY-MM-DD")
        try:
            dt.date.fromisoformat(item["accessed"])
        except (ValueError, TypeError) as exc:
            raise Invalid("source.accessed: expected YYYY-MM-DD") from exc
    artifacts = keyed(data["artifacts"], "id path label kind", "artifacts")
    for item in artifacts.values():
        text(item["label"], "artifact.label")
        choice(item["kind"], {"image", "file"}, "artifact.kind")
        path = artifact_path(root, item["path"])
        if item["kind"] == "image":
            with path.open("rb") as handle:
                header = handle.read(16)
            suffix = path.suffix.lower()
            valid = (suffix == ".png" and header.startswith(b"\x89PNG\r\n\x1a\n")
                     or suffix in {".jpg", ".jpeg"} and header.startswith(b"\xff\xd8\xff")
                     or suffix == ".gif" and header.startswith((b"GIF87a", b"GIF89a"))
                     or suffix == ".webp" and header[:4] == b"RIFF" and header[8:12] == b"WEBP")
            require(valid, "image artifacts must be PNG, JPEG, GIF or WebP with matching bytes")
    observations = keyed(data["observations"], "id actor method step_id action input observed outcome artifact_ids recorded_at settings", "observations")
    for item in observations.values():
        choice(item["actor"], {"agent", "user"}, "observation.actor")
        choice(item["method"], {"cli", "api", "browser", "desktop", "manual"}, "observation.method")
        slug(item["step_id"], "observation.step_id")
        require(item["step_id"] in steps, "observation.step_id does not exist")
        for key in ("action", "input", "observed", "settings"):
            text(item[key], f"observation.{key}")
        choice(item["outcome"], {"success", "failure", "partial"}, "observation.outcome")
        references(item["artifact_ids"], artifacts, "observation.artifact_ids")
        instant(item["recorded_at"], "observation.recorded_at")
        if item["actor"] == "user":
            require(item["method"] == "manual", "user observations use manual; record agent tool runs as agent")
        else:
            require(item["method"] != "manual", "agent observations require an actual execution method")
            require(capabilities.get(item["method"]) == "available", f"observation requires available {item['method']} capability")
    checks = {}
    for item in seq(data["verification"], "verification"):
        obj(item, "check status observation_ids detail", "verification")
        choice(item["check"], CHECKS, "verification.check")
        require(item["check"] not in checks, "duplicate verification check")
        checks[item["check"]] = item
        choice(item["status"], {"passed", "failed", "unverified"}, "verification.status")
        references(item["observation_ids"], observations, "verification.observation_ids")
        text(item["detail"], "verification.detail")
        if item["status"] == "passed":
            require(bool(item["observation_ids"]), "passed checks require observations")
            for ref in item["observation_ids"]:
                obs = observations[ref]
                require(obs["outcome"] == "success" and bool(obs["artifact_ids"]), "passed checks require successful observations with saved evidence")
    for key in ("limitations", "next_steps"):
        texts(data[key], key)
    for note in keyed(data["notes"], "id created_at text", "notes").values():
        instant(note["created_at"], "note.created_at")
        text(note["text"], "note.text")
    if data["status"] == "ready":
        require(data["entry"] is not None, "ready requires an entry")
        require(all(r["status"] == "available" for r in data["requirements"]), "ready requires available resources")
        require(set(checks) == CHECKS and all(c["status"] == "passed" for c in checks.values()), "ready requires entry, sample, core-action and reset checks")
        if data["mode"] == "agent-demo":
            demonstrated = {o["step_id"] for o in observations.values()
                            if o["actor"] == "agent" and o["artifact_ids"]}
            require(set(steps) <= demonstrated,
                    "agent-demo requires saved agent evidence for every planned step")
    return data


def atomic_write(path, content):
    path = Path(path)
    require(not path.is_symlink(), f"refusing to replace symlink: {path}")
    require(not path.exists() or path.is_file(), f"not a file: {path}")
    fd, temp = tempfile.mkstemp(prefix=f".{path.name}-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def write_bundle(root, data, source=False):
    from render_page import render_page
    validate(data, root)
    canonical = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    require(len(canonical.encode("utf-8")) <= MAX_JSON,
            f"serialized bundle exceeds {MAX_JSON} bytes; no files changed")
    page = render_page(data)
    for name in ("index.html", "experience.json"):
        target = root / name
        require(not target.is_symlink(), f"{name} is a symlink")
        require(not target.exists() or target.is_file(), f"{name} is not a regular file")
    if source:
        atomic_write(root / "experience.json", canonical)
    atomic_write(root / "index.html", page)


def new_bundle(root, title, kind, target_url, language):
    root = Path(root).absolute()
    require(not root.exists() and not root.is_symlink(), "new requires a destination that does not exist")
    require(root.parent.is_dir(), "create the output parent directory first")
    identifier = re.sub(r"[^a-z0-9]+", "-", root.name.lower()).strip("-")[:60] or "experience"
    identifier += "-" + os.urandom(4).hex()
    unknown = "Not assessed yet."
    data = dict(schema_version=1, id=identifier, title=title, language=language, kind=kind,
                mode="self", status="draft", summary="Experience preparation has not started.",
                goal="Choose one thing to learn by using this project.",
                target=dict(name=title, url=target_url, version=unknown),
                budget=dict(preparation=unknown, hands_on=unknown, cost="No new paid resources authorized."),
                authorization=dict(scope="Read-only investigation and bundle authoring.", constraints=["Confirm any additional resource use not already authorized."]),
                requirements=[dict(name="Target access", status="unknown", detail=unknown)], capabilities=[], entry=None,
                baseline="Identify and prepare a reproducible starting state.", reset="Document and verify a way back to the starting state.",
                steps=[dict(id="first-try", title="Define the first useful action", instruction="Replace this draft with a concrete action for the selected project.", input="Prepare a usable sample.", expected="Describe what to observe, without predicting success.", variations=[])],
                sources=[], artifacts=[], observations=[], verification=[], limitations=["No product operation has been verified."], next_steps=["Investigate the target and complete the experience plan."], notes=[])
    staging = Path(tempfile.mkdtemp(prefix=".experience-", dir=root.parent))
    try:
        (staging / "artifacts").mkdir(mode=0o700)
        write_bundle(staging, data, source=True)
        require(not root.exists(), "destination appeared during creation; preserving it")
        staging.rename(root)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return data


def import_notes(root, data, path):
    envelope = load_json(path)
    obj(envelope, "schema_version experience_id note", "notes import")
    require(type(envelope["schema_version"]) is int and envelope["schema_version"] == 1, "unsupported note version")
    require(envelope["experience_id"] == data["id"], "notes belong to another experience")
    note = envelope["note"]
    keyed([note], "id created_at text", "notes")
    instant(note["created_at"], "note.created_at")
    text(note["text"], "note.text")
    for existing in data["notes"]:
        if existing["id"] == note["id"]:
            require(existing == note, "note id already exists with different content; preserving both files")
            return False
    data["notes"].append(note)
    write_bundle(root, data, source=True)
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    new = subs.add_parser("new", help="Create a draft bundle; does not run the target")
    new.add_argument("bundle", type=Path)
    new.add_argument("--title", required=True)
    new.add_argument("--kind", choices=sorted(KINDS), required=True)
    new.add_argument("--target-url", required=True)
    new.add_argument("--language", choices=["en", "zh-CN"], default="en")
    for name in ("validate", "render", "import-notes"):
        command = subs.add_parser(name)
        command.add_argument("bundle", type=Path)
        if name == "import-notes":
            command.add_argument("notes", type=Path)
    args = parser.parse_args(argv)
    try:
        root = args.bundle.absolute()
        if args.command == "new":
            data = new_bundle(root, args.title, args.kind, args.target_url, args.language)
        else:
            data = validate(load_json(root / "experience.json"), root)
            if args.command == "render":
                write_bundle(root, data)
            elif args.command == "import-notes":
                import_notes(root, data, args.notes)
        print(json.dumps({"status":data["status"], "bundle":str(root), "command":args.command}, ensure_ascii=False))
        return 0
    except (Invalid, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
