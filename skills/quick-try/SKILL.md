---
name: quick-try
description: Turn a model, coding agent, product, or prompt collection into a prepared hands-on trial with a capability check, agreed plan, usable sample, durable guide, and optional agent walkthrough. Use when someone wants to try or evaluate something by operating it; ordinary explanations and production implementation are outside this skill.
---

# Quick Try

Turn something the user wants to explore into a ready-to-use scene. First establish what this host can actually research, prepare, and operate; then agree on the approach before changing the environment or running the target. Do the preparation and optional demonstration while leaving exploration and personal judgment to the user. Deliver a durable experience page with inputs, steps, expectations, evidence, and a way to start again. Conversation coordinates the work rather than becoming its only record.

## Reconnoiter before proposing the trial

Inspect the supplied project and the user's question before choosing a setup. Resolve the actual project, version, and official usage path; similar names are not interchangeable. Let a concrete question guide the scene, for example: "What happens when I change the requirement while this coding agent is working?" For free exploration, recommend one approachable question and a few optional changes. Ask early only when ambiguity prevents meaningful reconnaissance.

Perform read-only capability discovery relevant to that question:

- **Sources:** current first-party documentation, general Web research, and any installed social or community search skill, connector, or tool. Distinguish platform-aware search from ordinary Web results and authenticated access from public access. Read [Source and social discovery](references/source-discovery.md) when other users' practice, examples, or reactions could change the trial.
- **Agent-run trial:** identify the actions an agent could perform to answer the trial question, then inspect the callable capabilities needed for those actions. Choose among local files, shell, structured APIs, model calls, browser interaction, desktop interaction, or user-operated steps by fitness for the question. A product name, installed package, or old run does not prove current access.
- **Environment:** determine exactly how far Quick Try can prepare the target before the user arrives. Inspect the target checkout or account, runtime, dependencies, sample data, ports or services, persistence, first action, and a safe reset or fresh baseline. Read manifests and help before proposing installation or startup commands.
- **Resources and effects:** credentials or takeover, private data, cost or quota, downloads and installation, external writes, messages, publishing, and expected preparation time.

Unknown remains unknown. Capability discovery does not install a plugin, connect an account, grant permissions, expose credentials, make a paid call, mutate the target, or begin the proposed demonstration.

Choose the least preparation that preserves the target behavior: an existing demo, the original product, an API or CLI task, a prepared local app, or an isolated environment. Keep original interaction when interaction is the subject. Samples may be synthetic when their purpose and limits are clear. A simulation, prerecorded output, substituted model, or recreated interface cannot prove the original product's behavior.

## Present the preflight report and agree on the plan

Read [Preflight report](references/preflight-report.md) and present it before material environment preparation or target execution. Write for a user who may know nothing about the project. Explain the project first, then say how ready the experience can be, offer concrete scenes with prepared data, describe what the agent will run, and report useful signals from other users. Keep capability and evidence details available without making them the main reading path.

Recommend one scene while giving the user meaningful alternatives when the target supports them. State whether the proposed mode is **Self** or **Agent demo**, what will be ready at handoff, what still needs takeover, and how each limitation changes the result. Include preparation and hands-on time estimates plus cost or quota assumptions.

Ask the user to confirm or correct the report before dependent preparation and execution. The report is one meaningful gate, not a series of confirmations. After confirmation, continue routine actions within the agreed plan without asking again. If later discovery introduces a material new dependency, cost, account action, environment change, private-data use, or external effect, report only that delta and obtain the missing decision before the dependent action; continue unaffected work.

Modes:

- **Self:** prepare and minimally verify the scene; the user explores it.
- **Agent demo:** additionally execute the agreed scene and preserve a reproducible walkthrough before handoff.

Default to Self when the user has not expressed a preference, but make the recommendation explicit in the preflight report. For Agent demo, first design the smallest useful sequence of actions, then choose the available methods that preserve the behavior being tested. No particular operation tool is a prerequisite for Quick Try.

Reuse the user's existing authorization when constructing the report. A choice already made in the request need not be asked again; reflect it as confirmed. Request only missing decisions, resources, or authority. Keep credentials in the host's appropriate credential mechanism. Record the connection name and requirements, not tokens, session cookies, private account details, or authentication screenshots. Authentication and account verification may require the user to take over.

After confirmation, prepare the agreed environment to the promised level and transfer the findings into the bundle's target, budget, authorization, requirements, capabilities, steps, limitations, and reset fields so the plan survives the conversation. The handoff must give the user a direct entry with the sample already available and an obvious first action.

## Prepare the matching trial

Read only the matching recipe:

- Model or prompt collection: [Models and prompts](references/models-and-prompts.md).
- Coding agent or harness: [Coding agents](references/coding-agents.md).
- Interactive product: [Products](references/products.md).
- When the trial depends on browser or desktop interaction: [Interface operation](references/interface-operation.md).

This skill authorizes neither its own installation nor publication of a report or environment. Public skill distribution and a user's private experience bundle are separate activities.

## Prepare and prove usability

Use a task-owned location and preserve existing files and processes. Prepare samples, entry instructions, a short first action, optional variations, and observable expectations. Keep a baseline that can be restored without overwriting unrelated work. Record target version and settings that affect reproducibility.

Preparation is complete only when evidence demonstrates all four checks:

1. **Entry:** the actual experience entry is reachable and usable.
2. **Sample:** the intended data or material is loaded and usable.
3. **Core action:** at least one meaningful action relevant to the question executes and produces an inspectable result.
4. **Reset:** the starting state can be restored or a fresh equivalent instance has been created and verified.

An HTTP response, installation log, plan, or screenshot of a landing page alone cannot satisfy these checks. Evidence may be a result file, selected log, screenshot, or recorded manual verification. A disappointing product result can still establish a usable scene; a broken execution path cannot. Preserve the demonstrated output before resetting or duplicating the baseline for the user.

In agent-demo mode, also execute each agreed demonstration step and record its actual outcome and evidence. An unexecuted required step keeps the promised walkthrough blocked even when the environment is available. Optional variations can remain for the user. Structural validation checks that each planned step has an artifact-backed agent observation; it cannot establish that those observations actually demonstrate the promised behavior.

If the user will perform a resource-dependent action later, keep that check unverified and the bundle draft or blocked. Do not mark the scene ready merely because its instructions are complete. Required resources belong in requirements; optional possibilities belong in limitations or next steps.

Stay within the agreed preparation, spending, and repair scope. Stop the current path when its budget is reached or repeated failure yields no new evidence. Retry only with a changed hypothesis or a known transient condition, within the remaining allowance. Avoid repair that becomes replacement of the target's core behavior.

## Deliver a durable experience

Read [Bundle format and commands](references/bundle-format.md) before creating or updating the deliverable. Its schema and CLI are the source of truth. With Python 3.10+, use the bundled standard-library script to create, validate, and render an offline `index.html` from `experience.json`; keep selected inputs, outputs, screenshots, and logs under `artifacts/`.

The page is a guide, evidence viewer, and navigation point. The actual product can remain in its own app, website, or terminal. The page does not run arbitrary commands, hold API keys, or promise a permanent local server. Preserve start, stop, and resume instructions for an environment whose lifetime differs from the page's.

Write the experience in the user's language and replace the generated draft's English scaffold before handoff. The renderer currently localizes interface labels for English and Simplified Chinese; authored content remains the agent's responsibility. Keep explanations concrete: what to do, what changes, and what to observe. Put goal, resources, and reset within easy reach; keep deep background optional. Separate expected behavior from actual observations, project claims from community reports, and agent observations from the user's feelings. A demonstration report describes what the agent did, not the user's personal experience.

Validate the bundle and inspect the rendered page using an available browser when possible. Check the actual start/reference entry, sample links, evidence, and notes export/import. Page validation checks structure, not truth; retain evidence for readiness. If Python is absent, provide the same information and artifact links as a durable Markdown guide, preserve the JSON for later rendering, and identify the unavailable rendering and validation steps. Do not install a runtime solely for presentation without authorization.

Notes must survive the conversation: export browser drafts and import them into the bundle, or append the user's notes through the canonical authoring workflow. Explain that an unexported browser draft is not saved to disk. Preserve raw results and the user's own wording when helping organize a future sharing post.

Handoff includes the experience file, actual readiness, first action, known limitations, and how to reset or continue. A local or temporary URL is available only for its verified environment lifetime. Avoid automatically publishing or uploading the bundle.

## Handle limits constructively

For a missing account, tool, permission, service, or hardware resource, deliver the completed preparation and say exactly what remains blocked and how to resume. When UI tools are unavailable, offer user-operated steps or another execution method only if it can answer the same question; preserve the original goal when it cannot.

Production hardening, ongoing hosting or monitoring, large product rewrites, broad benchmark claims, and writing or publishing a first-person review on the user's behalf require separate scope. Small setup adapters and sample preparation belong here when they preserve the behavior being explored. Refuse only the disallowed action when a request requires bypassing access controls, fabricating evidence, or exposing credentials; continue a useful permitted alternative when one exists.

Every paused or unsuccessful handoff states what was completed, the concrete blocker, its effect on the question, and the next viable step. Partial work remains partial in both the page and the final response.
