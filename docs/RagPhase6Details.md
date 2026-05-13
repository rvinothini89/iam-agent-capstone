# Phase 6: Planning, Memory & Context

## Objective

Enhance the IAM agent to support:

* Multi-step reasoning and planning
* Short-term and long-term memory
* Context-aware multi-turn conversations
* Memory retention and reset behavior
* Improved conversational quality

---

# Features Implemented

## Multi-Step Reasoning (Planning)

The agent follows a structured reasoning workflow before making decisions.

### Planning Steps

```json
"plan": [
  "Extract attributes from input",
  "Merge with memory state",
  "Retrieve policies",
  "Evaluate compliance",
  "Final decision"
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

## Components

### Conversation History

Stores previous user-agent interactions during the session.

### Structured State

```python
state = {
  "role": None,
  "access_type": None,
  "resource": None
}
```

## Purpose

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

## Purpose

* Retain state across sessions
* Improve continuity
* Demonstrate persistent context handling

---

# Memory Retention Rules

The following retention behavior was implemented:

| Rule                     | Behavior                                      |
| ------------------------ | --------------------------------------------- |
| Session continuity       | Memory retained during ongoing request flow   |
| Relevant context only    | Only role, access_type, and resource retained |
| Latest input wins        | New inputs override previous state            |
| Reset support            | User can explicitly clear memory              |
| Stale context prevention | New requests do not blindly reuse old state   |

---

# Memory Reset Behavior

The agent supports explicit memory clearing.

### Example

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

The agent combines:

* Current user input
* Conversation history
* Structured state

to complete incomplete requests across multiple turns.

---

# Demonstration: Improved Conversation Quality

---

# Before (Without Memory)

The agent behaved statelessly and repeatedly asked for the same information.

```text
User: I need access
Agent: Please provide role and access type

User: QA
Agent: Please provide role and access type ❌

User: write access
Agent: Please provide role and access type ❌
```

---

# After (With Memory + Planning)

The agent now remembers previous inputs and asks only for missing information.

### Example 1: QA Write Access Request

```text
User: I need access
Agent: Please provide role and access type

User: QA
Agent: Please provide access type

User: write access
Agent: Escalating request for approval
```

### Actual execution output: 

```json
Response:
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

### Conversation Flow

```text
User: I need access
User: dev
User: read access, test db
```

### Actual execution output: 

```json
Response:
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

## Behavior

* If required attributes already exist in memory:

  * Do not ask again
  * Continue evaluation

## Benefit

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
