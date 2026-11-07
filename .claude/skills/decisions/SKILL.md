---
name: decisions
description: Lists every decision made for the user on the current change, challenges each with the skeptic subagent, and persists rejections as rules. Start with /decisions.
disable-model-invocation: true
---

# Decisions You Didn't Make

When started with `/decisions`, inspect all recent changes and execution trajectory.

## Workflow

1. **List all decisions:**
   Enumerate every choice made on this change:
   - Defaults chosen
   - Features, checks, or files left out
   - Requirements that were reinterpreted or narrowed
   *Avoid:* Grouping decisions together or labelling any decision as "minor".

2. **The Skeptic's Challenge:**
   For each individual decision, invoke the `skeptic` subagent (or adopt its persona) to argue the other side in exactly two sentences.

3. **User Selection:**
   Present each decision and challenge to the user for a verdict (Accept or Reject).

4. **Rule Persistence:**
   When the user rejects a decision:
   - Prompt them for the reason if not already stated.
   - Append exactly one line to `CLAUDE.md` with the permanent rule and the user's reason so future tasks do not repeat it.
