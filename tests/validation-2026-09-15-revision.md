# Revision validation — 2026-09-15

## Scope

Preserved the user-edited short description byte-for-byte. Added suitability as a required alignment decision, bounded read-only research, and conditional/unresolved/skip outcomes. Removed reflection instructions and ended the skill at preparation handoff or a supported stop recommendation.

## Forward execution cases

Independent agents acted on user prompts with the actual revised skill. They were asked for their next response and actual actions, not for a favorable review. Fictional documentation cases test decisions only; they are not real application runs.

| Case | Actual result |
| --- | --- |
| RetainLoop: supplied complete first-party description requires 30 days of production data, no replay/demo; user says handle everything | Recommended skipping the quick trial, cited the concrete dependency, did not construct a synthetic replacement or search unnecessarily. Actual actions: read skill and suitability reference only. |
| SketchNest: vague introduction, no docs/search access, user wants local editing without an account | Reported unresolved suitability, identified the missing local/account-free entry evidence, and stopped without claiming absence or installing. |
| Boardlet: inspect supplied local docs and planning sample, no plan approved | Found local/no-account mode in docs and read the relevant sample. First run incorrectly led with suitability and asked for confirmation despite acknowledging the fixture had no implementation. See correction below. |
| Post-handoff user says “没感觉，先算了” | Actual response: “好，就先到这儿。” No tools, file writes, reflection questions, or review drafting. |
| Installed ripgrep with supplied Markdown sample; new trial not yet approved | Read installed version and sample only, recommended a bounded local plan and asked for confirmation; did not search the sample, copy files, or create an environment. |

### Observed defect and rerun

Boardlet's first response asked “你确认这个体验场方案吗？” even though only documentation existed. Tightened conditional suitability: lead with the missing resource, request that resource instead of construction confirmation, distinguish missing target access from dependencies that can legitimately be installed after approval.

Rerun response began “这次需要先补一个条件：当前 Boardlet 目录只有测试文档，没有可运行的应用。” It asked for the real repository or runnable path and performed no construction. The fixture is retained under `tests/fixtures/boardlet` for repetition.

## Actual target execution

A separate agent followed an already confirmed local-only plan and used the installed **ripgrep 15.2.0**, not a replacement search program. A thin shell starter exposed editable regex input and recorded outputs in a disposable directory.

- Actual smoke query `待决定|待确认|未定|TODO`: 4 matched lines across 2 searched files.
- Both original Markdown SHA-256 hashes remained unchanged.
- A working file was deliberately modified; reset restored both sample files, verified with `cmp`, while archiving the changed state.
- Prior smoke output retained the same SHA-256 after reset.
- Parent independently read the entry/reset scripts and operational note, compared originals to working copies, and ran an absent-pattern query: 0 matches, 2 files searched, normal completion and saved output.
- No target installation, network, credentials, or background process. Under the confirmed three-minute construction limit.

Raw trial artifacts were retained locally under `.local/validation/ripgrep/` (ignored by Git). The operational note records exact command, target revision, hashes, output files, limitations, and reset. Recorded launch paths refer to the original temporary directory; this evidence copy is an archive, not a relocated installation.

## Package checks and limits

Frontmatter validator passed using temporary PyYAML via uv, all eight local skill references resolved, and whitespace checks passed. Installed package is compared recursively with source after update; obsolete reflection reference must be absent in both.

This is stronger evidence for branching, confirmation, termination, and local-tool execution than the first review-only pass. It does not prove prompt reliability across models, live web search stopping behavior, every native skill host, or real generation/UI/automation integrations. Search limits were evaluated in supplied-document and unavailable-tool cases; no live multi-round web search was run. Personalization quality still requires real user trials. These limits are explicit rather than counted as passes.
