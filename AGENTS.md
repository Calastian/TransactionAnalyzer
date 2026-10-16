# Agent Instructions

## Rules
- Minimize token usage. Be concise in reasoning, tool output, and responses.
- Inspect only files relevant to the current task. Never read the entire project by default.
- Prefer targeted searches and small file excerpts over dumping full files.
- Reuse existing code and patterns. Avoid unnecessary abstractions, dependencies, and refactors.
- Make the smallest change that solves the problem.
- Don't modify unrelated files or rewrite working code.
- Don't repeatedly inspect files or run commands without a clear reason.
- Run only the checks relevant to the changes made.
- Don't explain obvious steps or repeat information.
- Ask before making destructive, broad, or ambiguous changes.

## Workflow
1. Identify the relevant files.
2. Make the minimal required change.
3. Run a targeted check if needed.
4. Report only what changed and any important issues.

## Response Format
- Keep responses brief.
- Summarize changed files in one line.
- Include test results only when tests were run.
- Don't provide lengthy plans unless requested.
