---
name: friday
description: Weekly skill practice audit. Identifies the single skill or engineering muscle you have practiced least based on quiz logs, briefs, and git history. Start with /friday.
---

# The Friday Check

When started with `/friday`, evaluate the last 7 days of developer engagement and output a single-line audit.

## Inputs
1. `.claude/quiz/log.md` (past 7 days)
2. All briefs in `.claude/briefs/` (past 7 days)
3. `git log --since="7 days ago" --stat`

## Output Format
Write exactly **one line** naming the single skill or discipline practiced least, followed by the supporting evidence.

Example:
`Least-practiced skill: Error boundary design (Evidence: 3 missed quiz questions on lines 45-60, blank guess in brief 2026-11-04-auth).`

## Fallback
If there is insufficient data (e.g. fewer than 3 briefs/quizzes or brand new repository setup):
Output:
`Insufficient data: less than 7 days of quiz and brief logs available to evaluate skill practice.`

## Constraints
- Avoid giving advice.
- Avoid offering encouragement.
- Avoid listing multiple skills (choose the single most neglected skill).
- Do not invent metrics or facts.
