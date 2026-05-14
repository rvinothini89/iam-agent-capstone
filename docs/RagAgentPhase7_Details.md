# Phase 7: Adaptive Behaviour

## Objective

Enhance the IAM system with adaptive behavior capabilities across three personas:

* End User
* IAM Decision Agent
* IAM Security Agent

The goal of this phase was to allow the system to collect feedback, store it for future interactions, and modify future decisions using controlled adaptation logic.

---

# Persona Responsibilities

| Persona            | Responsibility                                                  |
| ------------------ | --------------------------------------------------------------- |
| End User           | Provides feedback about access decisions                        |
| IAM Decision Agent | Stores feedback and applies adaptive decision logic             |
| IAM Security Agent | Ensures adaptive decisions remain controlled and security-aware |

---

# Feedback Collection

The End User can explicitly provide feedback.

## Example

```text id="4f4xw0"
feedback: qa write access test_db should be approved
```

The IAM Decision Agent captures and stores this feedback for future evaluations.

---

# Feedback Storage

Feedback is persisted in:

```text id="y3wfxn"
feedback_store.json
```

## Example

```json id="jlwmqa"
[
  {
    "feedback": "qa write access test_db should be approved"
  }
]
```

---

# Adaptive Behaviour Flow

```text id="jlwmqb"
End User
    ↓
IAM Decision Agent
    ↓
Policy Evaluation
    ↓
Feedback Adaptation Layer
    ↓
IAM Security Agent Validation
    ↓
Final Decision
```

---

# Behaviour Modification

The IAM Decision Agent applies stored feedback to modify future decisions.

---

# Before Feedback

## Input

```text id="jlwmqc"
QA need write access to test db
```

## Output

```json id="jlwmqd"
{
  "decision": "deny"
}
```

The IAM Security Agent denied the request because the original policy did not permit QA write access to `test_db`.

---

# Feedback Provided

## Input

```text id="jlwmqe"
feedback: qa write access test_db should be approved
```

---

# After Feedback

## Input

```text id="jlwmqf"
QA need write access to test db
```

## Output

```json id="jlwmqg"
{
  "decision": "approve",
  "reason": "Behavior adapted based on previous feedback"
}
```

The IAM Decision Agent modified the behavior using stored feedback while the IAM Security Agent validated the adjusted decision.

---

# What Changed?

| Before               | After                          |
| -------------------- | ------------------------------ |
| Strict policy denial | Feedback-adjusted approval     |
| Static behavior      | Adaptive behavior              |
| No learning          | Feedback-aware decision-making |

---

# Failure Mode Identified

A role extraction issue was discovered during implementation.

## Problem

Substring matching incorrectly detected:

```text id="jlwmqh"
"dev" inside "need"
```

This caused incorrect role assignment.

---

# Resolution

Regex word-boundary matching was implemented:

```python id="jlwmqi"
re.search(r"\bdev\b", text)
```

This improved extraction accuracy and prevented unintended persona behavior.

---

# Outcome

| Capability                     | Status      |
| ------------------------------ | ----------- |
| Feedback collection            | Implemented |
| Feedback persistence           | Implemented |
| Adaptive decision behavior     | Implemented |
| Persona-aware adaptation       | Implemented |
| Controlled security validation | Implemented |

---

# Final Summary

Phase 7 introduced adaptive behavior into the IAM system using persona-driven feedback workflows.

The End User provides feedback, the IAM Decision Agent stores and applies adaptation logic, and the IAM Security Agent ensures that adaptive decisions remain controlled and security-aware.
