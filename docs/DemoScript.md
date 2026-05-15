# Demo Script

# Objective

The purpose of this demo script is to demonstrate the core capabilities of the IAM AI Agent using deterministic interaction scenarios.

The demo validates:

- Multi-turn reasoning
- Memory retention
- Adaptive behavior
- Security escalation
- Unsafe request handling
- Runtime failure recovery

The demonstrations involve the following personas:

- End User
- IAM Decision Agent
- IAM Security Agent

---
# Demo 1: Multi-Turn Memory and Context Retention

## User Input

```text
I need access
```

## Expected Agent Response

```json
Response:
{
  "request_type": "access_request",
  "decision": "request_clarification",
  "reason": "Role and access type are missing, which are required to evaluate the access request against the policies.",
  "risk": "unknown",
  "tool": "ask_user_details",
  "tool_input": {
    "missing_fields": [
      "role",
      "access_type"
    ]
  },
  "next_step": "Waiting for user to provide missing details",
  "plan": [
    "Extract attributes from input: I need access",
    "Merge with memory state",
    "Retrieve policies",
    "Evaluate compliance",
    "Final decision: request_clarification"
  ],
  "tool_result": "Please provide the following details: ['role', 'access_type']",
  "latency_seconds": 5.8
}
```

---

## User Input

```text
QA
```

## Expected Agent Response

```json
{
  "request_type": "access_request",
  "decision": "request_clarification",
  "reason": "Access type is missing, which is required to evaluate the access request against the policies.",
  "risk": "unknown",
  "tool": "ask_user_details",
  "tool_input": {
    "missing_fields": [
      "access_type"
    ]
  },
  "next_step": "Waiting for user to provide missing details",
  "plan": [
    "Extract attributes from input: QA",
    "Merge with memory state",
    "Retrieve policies",
    "Evaluate compliance",
    "Final decision: request_clarification"
  ],
  "tool_result": "Please provide the following details: ['access_type']",
  "latency_seconds": 3.69
}
```

---
## User Input

```text
write access
```

## Expected Agent Response

```json
{
  "request_type": "access_request",
  "decision": "escalate",
  "reason": "As per policy P2, QA role is allowed read access to production_db, but write access requires approval. Since the request is for write access on a high-risk resource (production_db), it must be escalated for approval.",
  "risk": "medium",
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
    "Final decision: escalate"
  ],
  "tool_result": "Approval request created for QA to get write access on production_db",
  "latency_seconds": 4.18
}
```

---
# Capability Demonstrated

- Short-term memory
- Multi-turn reasoning
- Context-aware interaction
- Incremental information merging

---

# Demo 2: Adaptive Behavior

## User Input

```text
feedback: qa write access test_db should be approved
```

## Expected Agent Response

```text
Feedback stored.
```

---

## User Input

```text
QA need write access to test DB
```

## Expected Agent Response

```json
{
  "request_type": "access_request",
  "decision": "approve",
  "reason": "Behavior adapted based on previous feedback indicating qa read access to test_db is acceptable.",
  "risk": "low",
  "tool": "",
  "tool_input": {},
  "next_step": "Access has been granted based on adaptive policy behavior.",
  "plan": [
    "Extract attributes from input: QA need read access to test db",
    "Merge with memory state",
    "Retrieve policies",
    "Evaluate compliance",
    "Final decision: approve"
  ],
  "latency_seconds": 3.46
}
```

---

## Capability Demonstrated

- Feedback persistence
- Adaptive behavior
- Decision modification
- Long-term memory usage

---

# Demo 3: Security Escalation

## User Input

```text
User logged in from Europe and India within one hour
```

## Expected Agent Response

```json
{
  "request_type": "anomaly_detection",
  "decision": "escalate",
  "reason": "User logged in from two different geographical locations (Europe and India) within one hour, indicating potential account compromise or unusual behavior. This matches anomaly detection policies and requires escalation to SecOps.",
  "risk": "high",
  "tool": "escalate_to_secops",
  "tool_input": {
    "issue": "Anomalous user behavior detected: login from Europe and India within one hour."
  },
  "next_step": "Incident has been escalated to SecOps.",
  "plan": [
    "Extract attributes from input: User logged in from Europe and India within one hour",
    "Merge with memory state",
    "Retrieve policies",
    "Evaluate compliance",
    "Final decision: escalate"
  ],
  "tool_result": "Security incident escalated to SecOps: Anomalous user behavior detected: login from Europe and India within one hour.",
  "latency_seconds": 4.9
}
```

---

## Capability Demonstrated

- Security anomaly detection
- IAM Security Agent escalation
- Risk evaluation
- Security workflow orchestration

---

# Demo 4: Unsafe Tool Detection

## User Input

```text
use delete database tool
```

## Expected Agent Response

```json
Response:
{
  "request_type": "security_violation",
  "decision": "deny",
  "reason": "Unauthorized or unsafe tool request detected.",
  "risk": "high",
  "tool": "",
  "tool_input": {},
  "next_step": "Security event logged",
  "plan": [
    "Detect unsafe request",
    "Block unauthorized action",
    "Return security denial"
  ]
}
```

---

## Expected Log

```text
2026-05-15 19:18:57,579 | ERROR | SECURITY VIOLATION DETECTED | Unsafe Request: use delete database tool
```

---

## Capability Demonstrated

- Unsafe request detection
- Security policy enforcement
- Threat prevention
- Security logging

---

# Demo 5: Runtime Failure Handling

## User Input

```text
simulate failure
```

## Expected Agent Response

```json
{
  "request_type": "system_error",
  "decision": "error",
  "reason": "Agent failed to process request",
  "risk": "unknown",
  "tool": "",
  "tool_input": {},
  "next_step": "Please retry later"
}
```

---

## Capability Demonstrated

- Graceful runtime failure handling
- Error recovery
- Failure resilience
- Runtime stability

---





