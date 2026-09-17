# File processing and developer tools

Use for CLIs, libraries, SDKs, formatters, search utilities, or coding tools whose benefit is an inspectable transformation or result. Select one operation relevant to the user's work, with input and output they understand.

Prepare a small fixture or isolated project copy with the actual minimum dependencies. Keep the original input and make output differences easy to inspect. For a library, a tiny editable example calling the real API is appropriate; avoid building an application around it merely to present a demo. A coding tool may need a runnable test and enough project context to preserve the problem.

Expose a useful choice: input, option, query, or code requirement. Provide the verified command in an interactive terminal or a task-local starter. Check one run on a duplicate; leave the sample ready for the user's own changes.

Stop if the trial becomes broad dependency repair or production integration. A benchmark library needs an actual timed measurement for performance claims, but ordinary quick trials need only the operation and visible result. Do not infer general speed or correctness from one sample.

An example scene is searching a small copied documentation set with a query the user actually cares about. They can change the query or inspect surprising matches, without following a numbered tutorial.
