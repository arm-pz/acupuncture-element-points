---
name: brief
description: Starts a new task brief by recording the user's intent before any work or proposals begin. Start with /brief <task-name>.
disable-model-invocation: true
---

# Brief

When the user starts a task with `/brief <task-name>`, capture their intent before proposing or writing any code.

## Questions to Ask
Ask these 3 questions and wait for the user's answers:
1. What does done look like?
2. What is your guess at the fix or design?
3. How will you know if it worked?

## Rules
- Avoid giving advice.
- Avoid answering for the user.
- Do not add extra questions.

## Storage
Save the responses to `.claude/briefs/<date>-<task-name>.md` where `<date>` is `YYYY-MM-DD`.

Format:
```markdown
# Brief: <task-name>
Date: <YYYY-MM-DD>

## 1. What done looks like
<user answer>

## 2. Guess at the fix or design
<user answer>

## 3. How we will know if it worked
<user answer>
```

Notify the user that the brief is recorded and must be read before proposing or writing anything.
