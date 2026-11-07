---
name: quiz
description: Tests the developer on recent diff lines before shipping to main. Unlocks push token only on a 5/5 score. Start with /quiz.
disable-model-invocation: true
---

# The 5-Question Quiz

When started with `/quiz`, verify that the developer genuinely understands the changes before pushing to `main`.

## Quiz Preparation
1. Inspect the diff: `git diff origin/main..HEAD` (or `git diff main..HEAD`).
2. Identify all non-blank, modified or newly added lines.
3. Select 4 distinct lines randomly from across the diff.
4. Formulate:
   - **4 questions** asking the developer what specific lines or logic do, why they were chosen, or what edge case they handle.
   - **1 question** asking what breaks if the core underlying assumption of this change is false.

## Ground Rules
- Ask the 5 questions **one at a time**.
- Provide **no hints**.
- Grade the developer's exact words strictly against the diff.
- For every incorrect or missed answer, display the exact line from the diff and explain the discrepancy.
- Log the date, final score (e.g., `4/5`), and any misses to `.claude/quiz/log.md`.

## Unlock Condition
- If and ONLY if the score is **5 out of 5**:
  Print the following unlock command for the user to run in their own terminal:
  ```bash
  mkdir -p .git/quiz-pass && touch .git/quiz-pass/$(git rev-parse HEAD)
  ```
- **CRITICAL:** NEVER run this command yourself. You are strictly forbidden by hook from modifying `.git/quiz-pass/`.
