# Quick Try

This repository maintains the portable [`quick-try`](skills/quick-try/SKILL.md) skill.

## Repository layout

```text
.
├── AGENTS.md
├── README.md
└── skills/
    └── quick-try/
```

The skill directory is self-contained. Its instructions, conditional references, renderer assets, helper scripts, and behavior tests travel together. Repository-level files only describe how the source is maintained.

## Validation

Run the skill's behavior tests from the repository root:

```sh
python3 -m unittest discover -s skills/quick-try/tests -v
```

When changing the generated reader, also run the browser check described in [`skills/quick-try/tests/README.md`](skills/quick-try/tests/README.md) and inspect its screenshots.

The repository does not contain prepared experiences or research results. Quick Try creates those in a task-owned output location when the skill is used.
