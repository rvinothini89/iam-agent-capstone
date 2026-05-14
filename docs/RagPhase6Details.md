# Phase 6: Planning, Memory & Context

## Objective

Enhance the IAM system with multi-turn reasoning and context-aware interactions across three personas:

* End User
* IAM Decision Agent
* IAM Security Agent

The goal of this phase was to improve conversational continuity, reduce repeated questioning, and support context-aware access evaluation.

---

# Persona Responsibilities

| Persona            | Responsibility                                                          |
| ------------------ | ----------------------------------------------------------------------- |
| End User           | Submits access requests and provides missing details incrementally      |
| IAM Decision Agent | Maintains memory, planning, and conversation state                      |
| IAM Security Agent | Applies security validation and risk evaluation using collected context |

---

# Features Implemented

## Multi-Step Reasoning (Planning)

The IAM Decision Agent performs structured reasoning before producing a decision.

### Planning Steps

```json
"plan": [
  "Extract attributes from input",
  "Merge with memory state",
  "Retrieve policies",
  "Evaluate compliance",
  "Generate Final decision"
]
```

### Purpose

* Makes decision-making transparent
* Improves explainability
* Enables debugging of agent reasoning flow

---

# Memory Implementation

The agent uses both:

* Short-term memory
* Long-term memory

---

# Short-Term Memory

The IAM Decision Agent stores:

* Conversation history
* Extracted user attributes
* Active request state

## Structured State

```python
state = {
  "role": "QA",
  "access_type": "write",
  "resource": "production_db"
}
```

### Purpose

* Track user attributes incrementally
* Avoid repeated questions
* Enable multi-turn conversations

---

# Long-Term Memory

## Implementation

Memory is persisted using:

```text
memory_store.json
```

This allows the IAM Decision Agent to retain relevant context across interactions.

### Purpose

* Retain state across sessions
* Improve continuity
* Demonstrate persistent context handling

---

# Memory Retention Rules

The IAM Decision Agent follows controlled memory retention behavior:

* Retain only relevant request attributes
* Use latest user input as highest priority
* Prevent stale context reuse
* Allow explicit memory reset

---

# Memory Reset Behavior

The End User can explicitly clear memory.

## Example

```text
User: reset
Agent: Memory cleared.
```

### Behavior

* Clears conversation history
* Clears structured state
* Prevents stale context reuse

---

# Context-Aware Multi-Turn Conversation

The IAM Decision Agent combines information incrementally across turns:

* Current user input
* Conversation history
* Structured state

to complete incomplete requests across multiple turns.

---

# Context-Aware Multi-Turn Interaction

The IAM Decision Agent combines information incrementally across turns.

## Example

```text
End User: I need access
IAM Decision Agent: Please provide role and access type

End User: QA
IAM Decision Agent: Please provide access type

End User: write access
IAM Security Agent: Escalating request for approval
```

---

# Demonstration: Improved Conversation Quality

## Before (Without Memory)

The agent behaved statelessly and repeatedly asked for the same information.

```text
User: QA
Agent: Please provide role and access type
```

Repeated clarification occurred because no context was retained.

---

## After (With Memory + Planning)

```text
User: QA
Agent: Please provide access type
```

The IAM Decision Agent remembered the previously provided role and only requested missing information.

---

# Example 1: QA Write Access Request

```text
User: I need access
Agent: Please provide role and access type

User: QA
Agent: Please provide access type

User: write access
Agent: Escalating request for approval
```

## Actual Execution Output

```json
{
  "request_type": "access_request",
  "decision": "escalate",
  "reason": "All required attributes available from state.",
  "risk": "high",
  "tool": "request_approval",
  "tool_input": {
    "role": "QA",
    "access_type": "write",
    "resource": "production_db"
  },
  "next_step": "Approval request has been sent to Manager",
  "plan": [
    "Extract attributes from input: write access",
    "Merge with memory state",
    "Retrieve policies",
    "Evaluate compliance",
    "Final decision: request_clarification"
  ],
  "tool_result": "Approval request created for QA to get write access on production_db"
}
```

---

# Example 2: Developer Read Access to Test DB

## Conversation Flow

```text
User: I need access
User: dev
User: read access, test db
```

## Actual Execution Output

```json
{
  "request_type": "access_request",
  "decision": "approve",
  "reason": "The access request is for 'read' access to 'test_db', which is allowed for the 'Developer' role as per policy P3. The risk is low since the resource is not classified as high-risk.",
  "risk": "low",
  "tool": "",
  "tool_input": {},
  "next_step": "Access has been granted.",
  "plan": [
    "Extract attributes from input: read access, test db",
    "Merge with memory state",
    "Retrieve policies",
    "Evaluate compliance",
    "Final decision: approve"
  ]
}
```

---

# State Enforcement Logic

The agent uses state enforcement to prevent repeated clarification loops.

### Behavior

If required attributes already exist in memory:

* Do not ask again
* Continue evaluation

### Benefit

* Eliminates infinite clarification loops
* Improves reliability
* Reduces redundant prompts

---

# Edge Cases Handled

| Scenario              | Handling                              |
| --------------------- | ------------------------------------- |
| Missing information   | Ask only missing fields               |
| Repeated prompts      | Prevented using state                 |
| Invalid context reuse | Prevented using reset logic           |
| Contradicting inputs  | Latest value overrides previous state |

---

# Conversation Quality Improvements

| Capability           | Before | After   |
| -------------------- | ------ | ------- |
| Context awareness    | ❌      | ✔       |
| Multi-turn reasoning | ❌      | ✔       |
| Memory support       | ❌      | ✔       |
| Repeated questioning | High   | Reduced |
| Decision continuity  | ❌      | ✔       |

---

# Outcome

| Requirement                   | Status         |
| ----------------------------- | -------------- |
| Multi-step reasoning          | ✔ Implemented  |
| Short-term memory             | ✔ Implemented  |
| Long-term memory              | ✔ Implemented  |
| Memory retention rules        | ✔ Implemented  |
| Memory reset behavior         | ✔ Implemented  |
| Improved conversation quality | ✔ Demonstrated |

---

# Final Summary

The IAM agent evolved from a stateless decision system into a context-aware intelligent assistant capable of:

* Multi-turn conversations
* Structured reasoning
* Persistent memory
* Incremental information gathering
* Context-aware access evaluation

The addition of planning, memory, and context handling significantly improved conversational quality and decision efficiency.
