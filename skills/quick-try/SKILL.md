---
name: quick-try
description: Prepare a personal, isolated hands-on trial for a user exploring a new project, tool, model, or agent.
---

# Quick Try

Help the user reach a meaningful interaction with a new project quickly. Use the project's stated promise to choose a small experience involving material the user cares about. Standardize the preparation; leave exploration and judgment to the user.

## 1. Understand and align

Read [suitability.md](references/suitability.md) during alignment. Decide whether this project can offer a worthwhile short experience for this user before proposing construction. Read the supplied project's README or official introduction and enough usage documentation to identify its core interaction and practical requirements. Treat stated benefits as hypotheses for the trial, without requiring a broad audit or community survey. Preserve the real target: a replica, substituted model, or simulated response is not experience of that target.

Have a brief conversation before preparation, usually one or two short exchanges followed by a plan. Ask one useful question at a time about what attracted the user, a relevant task or material, or constraints that would change the experience. Use answers already present instead of repeating questions or filling a questionnaire. If these are already clear, proceed to the plan confirmation.

During alignment, inspect only relevant, scoped, read-only information. Prefer user-supplied material and the current workspace. Read [materials.md](references/materials.md) when selecting a sample. Do not scan unrelated personal directories to manufacture personalization. No environment creation, installation, target execution, or private-data upload happens before the plan is confirmed.

Give a recommendation before advancing: suitable now, suitable if a named condition is met, not suitable for a quick trial, or unresolved after bounded research. Explain the concrete reason and next useful action. Only suitable projects advance to construction planning. Conditional projects may have a provisional plan, but unmet conditions remain explicit and block dependent construction. Stopping with a well-supported recommendation is a complete outcome of this skill.

## 2. Choose a recipe and propose the experience

Classify by what the user will actually do, not language, framework, or repository label. Read only the matching recipe; a mixed project uses the recipe for the selected core interaction:

| Core interaction | Recipe |
| --- | --- |
| Talk, revise, and collaborate over multiple turns with an agent or skill | [Collaboration](references/collaboration.md) |
| Process a file, change code, or call a library with inspectable results | [Developer tools](references/developer-tools.md) |
| Generate and revise text, images, audio, or other content | [Generation](references/generation.md) |
| Browse, arrange, search, edit, or play through a product interface | [Interactive apps](references/interactive-apps.md) |
| Run an automation once or replay a bounded input through its real pipeline | [Bounded automation](references/automation.md) |

Support depends on a short, authentic core loop, available resources, and a credible isolation boundary. If value requires days of use, production access, unavailable hardware, or extensive setup, say what cannot be experienced quickly. Offer an official accessible demo or a smaller authentic loop only when it preserves the selected promise. Guidance alone is preparation advice, not a ready experience.

Present one concise recommended experience in the user's language:

- **Possible change:** what the project promises to make different in a familiar task.
- **Your material:** the specific sample, why it fits, and any copying, redaction or external transmission.
- **What opens:** the real interface and prepared starting state, with room to choose what to do next.
- **Practical scope:** preparation estimate and limit, likely hands-on time, required takeover, cost/quota, isolation and exit route.

Aim for a small loop the user can explore in roughly 5–10 minutes; estimate honestly for the target. State a preparation time limit so setup cannot quietly become a repair project. Offer alternatives only when they materially change the experience.

**Ask the user to confirm this concrete plan and wait for their reply before construction.** An initial “try this” or “handle everything” is not confirmation of a plan they have not seen. An existing confirmation of the same plan carries forward. User revisions update the plan; resolve material changes before executing them. After confirmation, carry out routine preparation without repeated approvals. New cost, data transmission, or broader effects require only the missing decision.

## 3. Prepare and check

Read [preparation.md](references/preparation.md) before construction. Prepare the agreed sample, a disposable working state, and the simplest real entry supported by the host. Keep the original target's interaction when that interaction is what the user wants to experience.

Do a small smoke check of the entry and sample, and a representative core action when possible within the approved budget. Use a separate sample copy when checking would complete or spoil the user's task. Check how to stop and start fresh; retain useful results. A web response or installed binary alone does not demonstrate an operable trial.

Report exact readiness: **ready to explore**, **needs user takeover**, or **blocked**, with the concrete unverified part. A pending login or untested native skill activation is not a verified trial. Keep verification proportionate; no default benchmark, A/B run, evidence schema, or mandatory HTML report.

## 4. Hand over and leave room

Open or link one actual entry, with the sample at hand. Explain only what is ready, an optional first move, and how to stop or reset. Aim for one setup handoff; if the host requires more, disclose the real steps instead of promising a one-click experience.

Let the user choose their actions, change their mind, and stop early. Optional possibilities should emerge from the material, not a required sequence or turn count. Do not instruct them to perform staged interruptions or chase a predetermined result. Stay available for help; do not advance the target or consume their choices while they explore unless asked. A requested agent demonstration is valid but is recorded as agent observation, not user experience.

Keep a small private `TRIAL.md` in the trial directory with the confirmed plan, entry, sample origin, actual checks, and continuation/reset instructions. No webpage is required.

**This skill ends at the usable handoff or an honest suitability/blocker recommendation.** Do not initiate reflection, collect reactions, organize impressions, or draft a review. Subsequent requests to summarize information, discuss feelings, or help with the target are ordinary follow-up work outside this skill; do not restart alignment or append an experience questionnaire. A newly requested trial can invoke this workflow again.
