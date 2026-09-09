# Quick Try development

- `skills/quick-try/` is the canonical, self-contained skill source. Keep all runtime instructions, references, assets, and scripts inside that directory.
- Keep the repository root limited to source-maintenance files. Prepared experiences, research results, generated readers, and personal runs belong in ignored `.local/` or another task-owned location.
- Read `skills/quick-try/tests/README.md` before changing reader behavior. Run `python3 -m unittest discover -s skills/quick-try/tests -v` after changing the skill. For reader interaction or layout changes, also run its real-browser check and inspect the screenshots.
- Preserve actual observations and their provenance. Preparation, rendering, and structural validation do not constitute product-execution evidence.
- Keep credentials and machine-specific setup outside tracked files.
- Use `<type>/<short-description>` branches and commit completed parts separately.
