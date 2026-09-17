# Interactive products

Read for a Web app, desktop app, or other product whose workflow or interaction is the experience.

## Prepare a believable situation

Find the official product, current access path, and a suitable workspace or demo. Prefer the real product when its interaction is the question. Reimplementing a screenshot may teach a concept but cannot demonstrate the original product's usability.

Seed a small situation the user can recognize: a week with conflicting plans, a board with overdue tasks, or a document with unresolved comments. Include enough variation to reveal the product's behavior without filling the workspace with irrelevant data. Use test or synthetic data unless the user has authorized real material and its destination.

Select an operation with an observable outcome, then a useful alternative or edge case. Keep guidance brief enough to use beside the product. Let the user browse freely after the first step rather than requiring a rigid script.

## Respect the actual access path

Check current first-party documentation for signup requirements, demo limitations, quotas, data persistence, and available reset/export mechanisms. Features behind a paid tier remain unknown until access is verified; marketing copy does not establish usable access.

If the product requires authentication or account verification, prepare the surrounding materials and hand over that step to the user using the host's supported mechanism. Reuse only authorized sessions. Changing real shared workspaces, sending invitations or messages, buying subscriptions, and publishing content are distinct external actions; perform them only with applicable authorization.

Link the original product from the experience page rather than forcing it into an iframe. Cross-origin and login restrictions may prevent embedding, and replacing the interface can change the thing being explored. State whether the entrance is a demo, a local instance, or a user account, including any temporary lifetime.

## Evidence and reset

With UI operation available, follow [Interface operation](interface-operation.md). Preserve selected screenshots at meaningful transitions and the actual resulting state. The walkthrough should say what was clicked or entered, what changed, and what the user can try next. Avoid claiming that the agent's elapsed time measures a person's learning effort.

Without UI operation, prepare the samples and human steps. User-reported or user-supplied evidence may establish manual verification when attributed accurately. A page fetch or API response cannot establish a visual interaction that was never observed.

Keep an untouched copy or a tested reset procedure for seeded content. If the service cannot restore state, create an authorized fresh equivalent workspace or leave reset unverified and explain the consequence. Preserve outputs and selected evidence before cleaning up a task-owned workspace; account deletion is not a routine reset strategy.
