# Coding agents and harnesses

Read when preparing an experience of a coding agent, orchestration harness, or an agent development workflow.

## Prepare a comprehensible task

Use a small task-owned repository or an explicitly authorized copy of the user's project. Make its initial app and relevant checks work before invoking the target agent. Record the starting revision or a reproducible snapshot, task, baseline behavior, and acceptance condition. A project that fails before the agent acts cannot fairly demonstrate its coding ability.

Choose a task the user can inspect: change sorting behavior, add a small interaction, or fix a visible bug. When requirement changes are the question, define a natural interruption point and preserve the actual follow-up instruction. Keep some optional changes for the user rather than finishing every possible exploration in the demonstration.

## Use the actual harness

Resolve the official repository and usage documentation, inspect its checked-out version, and verify current commands with its own help or manifest. For example, [DeepSeek Harness](https://deepseek.com/harness/) is a first-party discovery entry, not a promise that a remembered setup command or feature still works. Open current documentation when using it and record the selected revision and execution mode.

Check prerequisites independently: model/provider access, dependencies, tool permissions, repository trust, and any nested agent environment. Only grant the target agent access needed for the agreed scene. Review startup or install actions as code before running them. Keep existing repositories, credentials, ports, and user-owned processes outside the disposable task boundary unless specifically authorized.

Prefer its original interface when evaluating interaction, progress, or intervention. CLI execution can establish code outcomes but does not establish that the Web UI is understandable. For comparisons, record differences in model, harness configuration, tools, environment, and task; describe an overall setup comparison when those factors cannot be held constant.

## Prove and show the outcome

Preserve the submitted task, meaningful interventions, selected execution evidence, patch, and relevant checks. Run the changed behavior when possible; inspect the resulting app as well as test output. A passing process exit alone is not proof that a requested feature works.

The experience page keeps the task and acceptance criteria visible while linking to the native agent UI, app preview, changed files, and evidence. Mark which checks the agent performed versus which the target harness reported. Attribute navigation/tool failures separately from failures in the generated code or product.

Before handoff, preserve the demonstration changes and provide a verified fresh baseline for the user's run. Use a task-owned copy, snapshot, or deliberately scoped restoration; do not reset unrelated user work. Record commands or procedures to start, stop, and resume the prepared services. Avoid promises that a process will remain running after the host session ends.

If the target needs extensive patches just to operate, stop at the agreed repair limit. Capture the blocking evidence and propose a narrower version or a separate repair task instead of silently evaluating a rewritten harness.
