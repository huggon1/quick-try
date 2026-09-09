# Models and prompt collections

Read for a new model, model comparison, or collection of reusable prompts. These recipes share input preparation, controlled changes, and result comparison; a prompt collection should additionally preserve the original case and its variables.

## Choose something the user can change

Prepare a concrete task, a usable input, and one small variation that might expose a useful difference. For text, this could be rewriting supplied notes and then introducing ambiguity. For image prompts, it could be changing a short title to a long title or changing one visual element while retaining the others. Let the user edit meaningful variables rather than confronting an empty box.

When the goal is casual exploration, one approachable example can be enough. For a requested comparison, use the same relevant input and settings where possible, record differences you cannot control, and preserve unsuccessful as well as successful results. Hidden model names can help compare subjective writing preferences, but a single task is not a general model ranking.

## Preserve the conditions

Resolve the actual provider and model identifier from its current official documentation or the configured service. Inspect available authenticated connections without exposing secrets. Verify input types, current access, generation limits, pricing assumptions, and output handling before execution. Model aliases and providers may change behavior; record the identifier used and the date, plus relevant parameters and seeds when supported. A seed is not a promise of identical future output.

For a prompt library, resolve its exact repository and revision. Preserve attribution, original wording, and reference-image usage conditions. Separate author examples from outputs generated during this experience. A gallery image does not establish that the same prompt works with a different model or version. Prefer a library's versioned source and the actual provider's documentation; discover those links from the target rather than keeping a universal provider catalog here.

Use API or CLI access when it answers the question; use a product interface when its interaction is part of the question. For a paid call, remain within confirmed budget and quota. If credentials or inference access are missing, prepare inputs and instructions but leave execution unverified. A mock response can illustrate presentation only and cannot count as model evidence.

## What the user should see

Keep the original input, editable variables, generation settings, and expected observation visible. Show actual output beside its input and previous attempt. Identify which condition changed between attempts. Preserve error messages or partial output relevant to the question, without dumping unrelated logs.

For image cases, use actual saved raster outputs or explicit reference links. Describe visual differences with the images available for inspection. For text, retain full selected output, not just the agent's favorable summary. Capture costs and latency only when available from an actual measurement or provider response; otherwise mark them unknown or estimated.

Reset means the user's next attempt starts from the prepared input and intended settings, while earlier results remain available. Reopening a blank chat without the samples is not an equivalent baseline.

## Related experiences

Look for posts with actual inputs and outputs relevant to this question, including failures. Record model/version/date differences. Turn a relevant observation into an optional variation rather than assuming the post's conclusion will reproduce. If none is credible or applicable, state that no useful community example was found instead of filling a quota.
