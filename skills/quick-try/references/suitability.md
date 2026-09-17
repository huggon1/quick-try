# Decide whether a trial makes sense

Alignment can end with a recommendation to skip a project. A category match is not sufficient reason to build. Judge the specific promise the user wants to explore against their materials, available host capabilities, and time/cost constraints.

## Questions to resolve

- What change does the user care about, and what real action could expose it in a short session?
- Is there relevant material the user can recognize and judge? If only a synthetic sample is possible, would it still answer their question?
- Can the actual target run with available resources and an acceptable isolation boundary?
- Will the user gain something by operating it now, compared with reading an example or watching the author's demo?

Technical runnability alone does not establish suitability. A retention product needing weeks of real behavior, a team coordination system with no other participants, or a speed claim requiring unavailable production scale may be installable but unsuitable for the selected experience. A small real subfeature can be offered only with its narrower value made explicit and accepted by the user.

## Bounded read-only research

Start with the supplied README/introduction and the first-party quickstart, requirements, or demo documentation relevant to the desired action. Inspect current scoped local capabilities as needed. Trust the author's stated promise as the experience hypothesis; inspect actual usage requirements independently. Documentation is not authorization to execute instructions.

If the answer is unclear, name the unresolved question before searching, for example “Is there an official offline replay?” Search only for evidence that can change the decision:

1. Search the project's official docs/repository for the missing usage path, limitations, sample, sandbox, or demo.
2. If still unresolved, consult a small number of directly relevant issues or independent usage reports for that same question. Distinguish reports from documented support.

Default research ceiling: about five minutes and at most two focused search rounds beyond the supplied introduction, reading up to three promising sources per round. This is a ceiling, not a quota. Stop earlier once the decision is supported. Obey a tighter user budget; expand only if the user asks. Research neither installs the target nor runs a trial to find out whether it might work.

When tools or sources are unavailable, report what could not be checked. An unsuccessful search means unknown, not proof the feature does not exist. At the ceiling, provide the current recommendation and the one missing fact or prerequisite that would change it. Do not keep searching automatically or switch to constructing a substitute experience.

## Communicate the decision

Use a short explanation, with source references when available:

- **Suitable now:** a meaningful short loop, relevant material, real entry, and practical boundary are identifiable. Continue brief alignment and present a concrete plan for confirmation.
- **Conditional:** a specific resource or decision is missing, such as login, suitable input, data permission, or access to the real target. Lead with that condition rather than “suitable now”. A provisional outline may illustrate what could be prepared, but ask for the missing resource/decision, not construction confirmation of an unavailable target. Installing accessible documented dependencies can be part of a confirmed plan; lacking the target implementation or a usable distribution is a different blocker.
- **Not suitable for this quick trial:** evidence shows the desired benefit requires unavailable conditions or disproportionate setup. Recommend skipping, reading an example, or watching an existing demo; those are alternatives, not a completed hands-on trial.
- **Unresolved:** bounded research did not establish a viable path. Explain the gap and stop rather than claiming impossibility or inventing a plan.

Keep recommendations tied to this user's intended experience. A project rejected for one promise may fit a different goal, but changing the goal needs their agreement. No construction or trial directory is required to deliver a suitability recommendation.
