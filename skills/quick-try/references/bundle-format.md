# Portable experience bundle

Read this when authoring, resuming, validating or handing off an experience. Python 3.10+ and its standard library are sufficient. The generated reader needs only a browser, including `file://`; it makes no model calls or network requests. Opening an explicit target/source link may access that service. This is a reader and record keeper, not a launcher or universal sandbox.

## Create and author

Resolve `SKILL_DIR` to this installed skill's directory using the host's skill location. Choose a new task-owned destination, outside the skill installation and outside any public checkout by default. Create its parent if needed. Shell-quote paths and titles using the host's safe argument API or shell quoting.

```sh
python3 "$SKILL_DIR/scripts/experience.py" new "$BUNDLE" \
  --title "Explore a project's core interaction" \
  --kind product --target-url https://example.org --language en
```

Use `model`, `harness`, `product` or `prompt`; page labels currently support `en` and `zh-CN`. The initial manifest is an English draft, even with Chinese interface labels. Replace its draft prose with the user's language and actual project information before handoff. Never pass a secret in command arguments or URLs.

The bundle contains:

```text
experience.json       Canonical plan, state, observations and imported notes
index.html            Generated offline reader; regenerate after changing JSON
artifacts/            Selected inputs, actual outputs, screenshots and logs
```

Edit `experience.json` as structured data rather than interpolating shell strings. Author plain prose, not HTML. Keep content concrete: what a person does, what changes, what they should look at. Separate expectations from observations. The renderer escapes all prose; Markdown syntax is not interpreted. Keep installation diagnostics and lengthy evidence out of the opening explanation.

```sh
python3 "$SKILL_DIR/scripts/experience.py" validate "$BUNDLE"
python3 "$SKILL_DIR/scripts/experience.py" render "$BUNDLE"
```

Neither command runs the target, installs dependencies or grants permissions. Structural validation checks completeness and references, not whether the reported experiment really happened. Preserve actual evidence and perform the selected scenario yourself when claiming verification.

## Manifest contract, version 1

Every listed field is required. Empty collections and `entry: null` are valid in an honest draft. Unknown fields are rejected so misspellings cannot silently disappear from the reader. IDs use lowercase letters, digits and hyphens, start with a letter or digit, and have at most 96 characters. IDs are unique within each collection. Individual strings have a 20,000-character limit; each collection has at most 200 elements; JSON has a 2 MiB limit.

| Field | Shape and meaning |
| --- | --- |
| `schema_version`, `id`, `title`, `language` | `1`, stable unique bundle slug, readable title, `en` or `zh-CN` |
| `kind`, `mode`, `status` | Kind above; `self` or `agent-demo`; `draft`, `blocked` or `ready` |
| `summary`, `goal` | Short orientation and the question or activity the user selected |
| `target` | `{name, url, version}`; identify exact project/model/revision; say when unknown |
| `budget` | `{preparation, hands_on, cost}`; text recording estimated effort and approved limits, not fabricated measurements |
| `authorization` | `{scope, constraints: [text]}`; summarize actual user authorization, including carried-forward approval; this record itself is not a grant |
| `requirements` | `[{name, status, detail}]`; status `available`, `missing` or `unknown`; resources actually required for this scenario |
| `capabilities` | `[{name, status, detail}]`; status `available`, `unavailable` or `unknown`; execution capability names `cli`, `api`, `browser`, `desktop` match observations; report evidence of actual host access |
| `entry` | `null` or `{label, url}`; a verified target link for ready scenarios; an unverified reference otherwise |
| `baseline`, `reset` | Starting data/state and an actionable restore or fresh-copy procedure; distinguish agent demonstration state from a user's fresh run |
| `steps` | `[{id, title, instruction, input, expected, variations: [text]}]`; at least one useful action; variations are optional |
| `sources` | `[{id, title, url, kind, accessed, context}]`; `kind` is `first-party` or `community`; `accessed` is `YYYY-MM-DD`; context explains relevance and limitations |
| `artifacts` | `[{id, path, label, kind}]`; bundle-relative `artifacts/...` path, `image` or `file`; existing regular files only |
| `observations` | See below; actual executions and human observations, not predictions or copied maker claims |
| `verification` | See below; traceable checks of the handoff |
| `limitations`, `next_steps` | Lists of plain text; disclose access failures, substitutions and untested branches |
| `notes` | `[{id, created_at, text}]`; user notes, preserved independently from agent observations |

An observation has exactly:

```json
{
  "id": "run-one",
  "actor": "agent",
  "method": "browser",
  "step_id": "first-try",
  "action": "Describe the actual action performed.",
  "input": "Identify the real input used.",
  "observed": "Describe the result actually observed, including failures.",
  "outcome": "success",
  "artifact_ids": ["result-one"],
  "recorded_at": "2026-09-08T10:00:00+08:00",
  "settings": "Record the relevant version, parameters and conditions."
}
```

The example illustrates structure, not a completed run. `actor` is `agent` or `user`. Agent methods are `cli`, `api`, `browser` or `desktop` and require the matching available capability. User observations use `manual`; identify user-supplied evidence honestly. `outcome` is `success`, `failure` or `partial`. An expected product failure can be a successful observation task if that was the actual goal; explain the distinction and preserve its result. Every `step_id` and `artifact_id` must resolve. Timestamps include an explicit timezone.

A verification entry has exactly `{check, status, observation_ids, detail}`. The four check names are `entry`, `sample`, `core-action` and `reset`; status is `passed`, `failed` or `unverified`. A passed check references one or more successful observations with saved artifacts. Evidence can be a command transcript or state/result screenshot as appropriate; a screenshot of the report itself does not prove target behavior.

`ready` requires all four checks passed, an entry and every required resource available. `agent-demo` also requires artifact-backed agent observations for every planned step. Put optional further experiments in `variations` or `next_steps`; additionally judge whether the observations actually cover the promised demonstration. The validator cannot judge whether a referenced artifact proves the check or whether prose is true. Never fill references merely to satisfy it. A user who verifies UI steps may provide manual records; the agent must not claim it performed those operations.

## Links and files

Target and source URLs accept HTTPS, or HTTP on literal `localhost`, `127.0.0.1` and `::1`. Credentials in URLs, script/data URLs, control characters and backslashes are rejected. After copying the actual local target into a bundle, both `target.url` and `entry.url` may point to an existing `artifacts/demo.html`; this is an explicitly opened target, never embedded untrusted markup in the reader. Do not leave a placeholder website as a local project's purported source.

Artifacts must stay inside the bundle's `artifacts/` directory without traversal or symlinks. Keep each file under 32 MiB. Images are PNG, JPEG, GIF or WebP with matching file signatures; SVG/HTML source is never embedded as an image. Video and other larger material may be linked externally if already authorized and usable, or represented by selected small evidence files; do not silently discard relevant failures. Renderer-generated pages contain inline CSS/JS and no external dependencies.

A bundle is private by default. Minimize screenshots and logs to the scoped target, inspect them for secrets/personal data, and redact selected copies while retaining an honest record of redaction. The tools do not automatically detect credentials. Publishing the skill does not publish bundles; publishing a bundle requires a separate authorized, reviewed share copy. Public URLs and license/attribution information are source references, not permission to redistribute third-party assets.

## Notes and resume

The reader's draft is not automatically written to disk. Export before refreshing or closing. Browser import loads an exported note into the draft, with an explicit replacement prompt if there is unsaved text. Import into the canonical bundle with:

```sh
python3 "$SKILL_DIR/scripts/experience.py" import-notes "$BUNDLE" /path/to/exported-note.json
```

The export envelope is `{schema_version: 1, experience_id: "bundle-id", note: {id, created_at, text}}`. Cross-experience notes are rejected. An identical repeated import is idempotent; a reused note ID with different content is rejected. New or edited drafts should export with a fresh ID. The CLI preserves existing notes and regenerates the reader. For a changed experience, keep the same ID only when it is the same exploration; a separate experiment gets a new bundle.

On resume, read the manifest and saved notes, confirm the target environment is still reachable, and preserve old observations. Historical `ready` is not a live health guarantee. Downgrade to `blocked` when a required resource expires or a core check no longer holds. Regenerate the page after changes. The reader shows recorded verification, not a live availability indicator.

If HTML publication fails after a canonical note update, retain the manifest and rerun `render`; do not discard notes to repair a derived page. Do not hand-edit generated HTML as the canonical record.

## No-Python fallback

Use the same goal, evidence and authorization rules. Save a readable Markdown experience guide with its inputs/results and honest verification status, plus a machine-readable record if practical. Explain that the bundled HTML renderer and structural validation were unavailable. This is reduced presentation capability, not permission to fabricate execution. Ask before adding a new runtime when that installation needs authorization; do not make an additional operation tool or Python installation a prerequisite for read-only planning.
