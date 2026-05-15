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
  "reason": "All required attributes recovered from memory state. Production access requires approval.",
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
    "Final decision: escalate"
  ],
  "tool_result": "Approval request created for QA to get write access on production_db",
  "latency_seconds": 3.26
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
  "decision": "approve",
  "reason": "Behavior adapted based on previous feedback"
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
  "decision": "escalate",
  "tool": "escalate_to_secops",
  "risk": "high"
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
{
  "request_type": "security_violation",
  "decision": "deny",
  "risk": "high"
}
```

---

## Expected Log

```text
ERROR | SECURITY VIOLATION DETECTED
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
  "decision": "error",
  "reason": "Agent failed to process request"
}
```

---

## Capability Demonstrated

- Graceful runtime failure handling
- Error recovery
- Failure resilience
- Runtime stability

---

# Engineering and Product Justification

# Why RAG Was Used

RAG was implemented to ensure policy decisions are grounded in retrievable IAM policy documents rather than relying only on LLM memory.

## Benefits

- Improved explainability
- Policy-grounded responses
- Reduced hallucination risk
- Better access governance

---

# Why Multi-Agent Personas Were Used

The architecture separates responsibilities across:

- End User
- IAM Decision Agent
- IAM Security Agent

## Benefits

- Clear workflow separation
- Improved reasoning orchestration
- Dedicated security escalation handling
- Better maintainability

---

# Why Memory Was Added

Short-term and long-term memory were implemented to:

- Reduce repetitive clarification
- Support multi-turn interaction
- Improve conversational continuity
- Maintain context across requests

---

# Why Adaptive Behavior Was Added

Adaptive behavior allows the system to:

- Store user feedback
- Modify future decisions
- Demonstrate controllable learning behavior

The implementation remains rule-driven for explainability and safety.

---

# Why Docker Deployment Was Used

Docker was selected to provide:

- Reproducible deployment
- Dependency isolation
- Environment consistency
- Simplified execution

---

# Why Logging and Tracing Were Added

Structured logging improves:

- Runtime observability
- Security auditing
- Failure debugging
- Operational monitoring

---

# Product-Oriented Considerations

The IAM agent was designed with:

- Explainability
- Security enforcement
- Risk awareness
- Controlled adaptation
- Operational traceability

These characteristics improve enterprise IAM suitability.

---

# Final Outcome

The IAM AI Agent demonstrates:

- Context-aware reasoning
- Multi-turn memory
- Adaptive behavior
- Security escalation workflows
- Runtime reliability
- Deployment readiness

The system combines AI-driven decision-making with IAM governance and operational safety controls.





