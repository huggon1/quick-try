# Maintainer validation

The skill itself requires only Python 3.10+ for HTML rendering. These checks do not install runtimes, operate third-party products, or establish the truth of authored observations.

Run structural, filesystem, readiness, rendering and notes regressions from the skill directory:

```sh
python3 -m unittest discover -s tests -v
```

For a browser check, use an already installed Node, Playwright and Chromium, and a small existing experience bundle:

```sh
node tests/browser_smoke.mjs /path/to/bundle /path/to/new-validation-output
```

The optional environment variables `QUICK_TRY_PLAYWRIGHT`, `QUICK_TRY_CHROMIUM` and `QUICK_TRY_PYTHON` select an existing Playwright module, browser executable and Python executable. Default resolution uses `playwright`, its configured Chromium, and `python3`. The output directory must not already exist; omit it to create a temporary directory. The test copies the bundle, exercises the reader and note round trip on that copy, and preserves screenshots plus JSON results for inspection. It does not open the target's external entry or call a model.

Browser assertions cover steps, accessible tabs, keyboard navigation, note download and import, invalid imports, literal markup, 1440/768/390-pixel layouts, no-JavaScript reading, and absence of HTTP requests or browser errors. Inspect the screenshots as well as the automated result. Test real target readiness and agent behavior separately, including a resource-blocked scenario and an actual successful walkthrough; structural tests cannot prove either.
