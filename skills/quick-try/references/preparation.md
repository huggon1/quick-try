# Prepare a usable, disposable trial

## Before construction

Proceed only after the concrete experience plan is confirmed. Read actual usage instructions and available tool schemas/help before selecting commands. Record the resolved target revision or version when available. Discover relevant capabilities cheaply; do not enumerate every installed integration.

Choose the smallest setup that preserves the target behavior: an official demo, an already installed target, a task-local dependency environment, or an isolated copy. Use the preparation limit stated in the plan. When it is reached, or repeated failure yields no new evidence, stop setup and explain the cause and viable next option. Further installation or repair beyond that limit needs a changed plan.

## Isolation

Create a new task-owned directory outside the original project and the distributed skill. Store sample copies, outputs, and `TRIAL.md` there. Use a separate environment/profile and disposable state supported by the target. Keep global agent configuration, original project data, and existing processes intact.

A temporary directory or Git worktree isolates file changes, not permissions, network access, credentials, or background services. Check the selected command's write paths and effects. Use available sandbox controls or a disposable runtime when needed; if the promised boundary cannot be provided, explain the actual limitation before running. Do not describe an unrestricted agent as sandboxed merely because its cwd is temporary.

For local servers, use an available port and track the exact process started for this trial. For external services, use approved test resources and state the cost and data scope. A replay or dry-run must be a real target-supported path. Disable external delivery using supported configuration; never invent fake outputs as proof of the target.

## Host adapter

Use the available path that preserves the chosen experience with the least setup burden:

1. Prepare a real target session or application state and open it, if the host permits those actions and the confirmed plan authorizes them.
2. Start an interactive CLI/session the user can actually take over. A detached process with no usable input surface is not an interactive handoff.
3. Prepare one starter command or file using verified target syntax. Keep it task-local and explain the single action needed.
4. Provide one complete starter prompt if only user-created chat is possible. Include target invocation, sample, and initial request together; say explicitly that opening a new chat and pasting are still required.

Do not hard-code a dependency on any host's task creation or browser API. Preserve skill loading semantics: pasting skill text into another prompt is an approximation unless that is the target's intended usage. Do not silently substitute it for native activation. Prefer a fresh session for behavior-changing skills; applying them to the coordinator can contaminate alignment and observations.

## Smoke check and handoff

Verify the actual entry is reachable, material is available in the target, and one meaningful action works where possible. Save a small useful result or diagnostic, not a comprehensive report. Keep the user's starting state fresh. For scarce paid actions, agree whether a smoke run is worth the cost; pending user execution remains unverified.

Check the supported stop/reset path or verify a fresh equivalent starting copy. Reset preserves prior outputs and changes only trial-owned state. Never offer broad deletion or terminate unrelated processes. Record environment lifetime and how to resume if the entry depends on a running process.

Use ordinary Markdown for `TRIAL.md`; adapt its length to the trial. Include the target, confirmed plan and limits, material source, real entry or starter, checks actually performed, remaining takeover, and stop/reset. This is an operational handoff record. Keep tokens and private credentials out. If the host cannot write files, supply a compact copyable record and state that it has not been saved to disk.

The handoff itself is short: entry, what is loaded, one optional starting action, and the relevant stop/limitation. Put technical detail in the note. User freedom begins once they enter: no automatic background A/B, scheduled monitoring, or continuation of their session without authorization.
