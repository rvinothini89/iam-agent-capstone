# Phase 7: Adaptive Behaviour

## Objective

Enhance the IAM agent to support adaptive behavior by:

* Collecting feedback from users
* Storing feedback for future interactions
* Modifying future decisions based on feedback
* Demonstrating behavioral improvement over time

---

# Features Implemented

## Feedback Collection

The agent accepts explicit user feedback using a feedback command.

### Example

```text
feedback: qa write access test_db should be approved
```

### Behavior

* Feedback is captured from user input
* Stored for future interactions
* Used to influence later decisions

---

# Feedback Storage

## Implementation

Feedback is persisted in:

```text
feedback_store.json
```

## Example Stored Feedback

```json
[
  {
    "feedback": "qa write access test_db should be approved"
  }
]
```

---

# Adaptive Behaviour Logic

The agent applies a feedback-driven adaptation layer after policy evaluation.

## Adaptation Flow

```text
User Request
    ↓
Policy Evaluation
    ↓
Feedback Adaptation Layer
    ↓
Final Decision
```

---

# Adaptation Strategy

If previous feedback indicates that a certain request is acceptable:

* The agent adjusts future decisions
* Overrides previous policy outcome
* Produces modified behavior

---

# Before vs After Behaviour

## BEFORE FEEDBACK

The base policy denied the request.

### Input

```text
QA need write access to test db
```

### Output

```json
{
  "decision": "deny",
  "reason": "Write access is not allowed for QA role"
}
```

### Explanation

* The original policy did not permit QA write access to `test_db`
* Decision was based strictly on policy rules

---

# FEEDBACK PROVIDED

### Input

```text
feedback: qa write access test_db should be approved
```

### Output

```text
Feedback stored.
```

---

# AFTER FEEDBACK

The same request now produces different behavior.

### Input

```text
QA need write access to test db
```

### Output

```json
{
  "decision": "approve",
  "reason": "Behavior adapted based on previous feedback indicating QA write access to test_db is acceptable.",
  "risk": "low"
}
```

---

# What Changed?

| Before                    | After                      |
| ------------------------- | -------------------------- |
| Request denied            | Request approved           |
| Strict policy enforcement | Feedback-adjusted behavior |
| No adaptation             | Adaptive decision-making   |

---

# Why the Behavior Changed

The agent detected stored feedback matching the current request context:

```text
QA + write access + test_db
```

Based on this feedback:

* The agent identified the request as acceptable
* The adaptive layer modified the original decision
* Final behavior changed from deny → approve

---

# Failure Mode Identified

During implementation, a role extraction issue was discovered.

## Problem

The logic:

```python
if "dev" in text
```

incorrectly matched:

```text
need
```

because `"dev"` existed as a substring.

This caused:

```text
QA need access
→ role incorrectly became Developer
```

---

# Resolution

Regex word-boundary matching was implemented:

```python
re.search(r"\bdev\b", text)
```

## Benefit

* Matches only complete words
* Prevents unintended role detection
* Improves extraction reliability

---

# Feedback Persistence

The stored feedback remains available across sessions because it is persisted in:

```text
feedback_store.json
```

This enables:

* Reusable adaptation
* Persistent learning behavior
* Context continuity

---

# Important Note

The agent does not retrain the LLM.

Instead:

```text
Behavior is modified using feedback-driven decision rules.
```

This provides controlled and explainable adaptation.

---

# Outcome

| Requirement                       | Status       |
| --------------------------------- | ------------ |
| Store feedback                    | Implemented  |
| Modify behavior based on feedback | Implemented  |
| Demonstrate before vs after       | Demonstrated |
| Explain adaptation logic          | Completed    |

---

# Final Summary

The IAM agent was enhanced with adaptive behavior capabilities using feedback-driven decision adjustment.

The agent can now:

* Store user feedback
* Reuse feedback in future evaluations
* Modify decisions dynamically
* Demonstrate behavioral improvement over time

This enables a more intelligent and context-aware access management workflow.
