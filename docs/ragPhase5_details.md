Phase 5: Tool Usage (Agentic Capabilities)
Overview

In this phase, the IAM agent is enhanced to select and execute tools based on its decisions. The agent now moves beyond reasoning and retrieval to taking controlled actions, while enforcing safeguards to prevent misuse.

Tools Defined

The agent supports the following tools:

1. request_approval(resource, role, access_type)
Used for high-risk access requests
Example: Write access to production systems
2. escalate_to_secops(issue)
Used for security anomalies
Example: Suspicious login patterns
3. ask_user_details(missing_fields)
Used when input is incomplete
Example: Missing role or access type
2. Tool Selection Logic
Decision	Tool Used	Description
approve	None	No action required
deny	None	Request rejected safely
escalate (access)	request_approval	Approval workflow triggered
escalate (anomaly)	escalate_to_secops	Security escalation
request_clarification	ask_user_details	Collect missing input
3. Correct Tool Usage Examples

Example 1: High-Risk Access Request

Input:
QA needs write access to production DB
Response:
{
  "request_type": "access_request",
  "decision": "escalate",
  "reason": "The request for write access to the production_db is not permitted for the QA role as per policy P2, which only allows read access. Additionally, production_db is considered high-risk, necessitating escalation for any access requests. Human approval is required for this action.",
  "risk": "high",
  "tool": "request_approval",
  "tool_input": {
    "resource": "production_db",
    "role": "QA",
    "access_type": "write"
  },
  "next_step": "Approval request has been sent to Manager",
  "tool_result": "Approval request created for QA to get write access on production_db"
}

Example 2: Low-Risk Access Request

Input:
Need read access to test database  
Response:
{
  "request_type": "access_request",
  "decision": "approve",
  "reason": "The user has requested read access to the test_db, which is allowed for the QA and Developer roles as per policy P3. The risk is low since the access type is read and the resource is not high-risk.",
  "risk": "low",
  "tool": "",
  "tool_input": {},
  "next_step": ""
}

✔ No tool invoked for safe operations

Example 3: Missing Information

Input:
I urgently need elevated access to production db for hotfix

Response:
{
  "request_type": "access_request",
  "decision": "request_clarification",
  "reason": "The role and access type are not specified in the request. Without this information, I cannot evaluate against the policies.",
  "risk": "unknown",
  "tool": "ask_user_details",
  "tool_input": {
  "missing_fields": [
  "role",
  "access type"
    ]
  },
  "next_step": "Waiting for user to provide missing details",
  "tool_result": "Please provide the following details: ['role', 'access type']"
}
Example 4: Anomaly Detection

Input:
User logged in from India and US within 1 hour

Response:
{
  "request_type": "anomaly_detection",
  "decision": "escalate",
  "reason": "User logged in from two different locations (India and US) within 1 hour, indicating potential anomalous behavior. This matches the anomaly detection policy for geo-velocity. Escalating to SecOps for further investigation.",
  "risk": "high",
  "tool": "escalate_to_secops",
  "tool_input": {
    "issue": "Anomalous user behavior detected: User logged in from India and US within 1 hour."
  },
  "next_step": "Incident has been escalated to SecOps.",
  "tool_result": "Security incident escalated to SecOps: Anomalous user behavior detected: User logged in from India and US within 1 hour."
}

4. Incorrect Tool Usage (Simulated)
Scenario: Wrong Tool Selection

Input:
Need read access to test database

Incorrect Output (Simulated):

{
  "decision": "approve",
  "tool": "request_approval"
}

Issue:
Approval tool was incorrectly invoked for a low-risk request.

Fix:
Updated prompt rules:

Approve/deny decisions must not trigger tools

Correct Behavior:

{
  "decision": "approve",
  "tool": ""
}

5. Invalid Tool Usage (Simulated)
Scenario: Non-Existent Tool

Simulated Output:

{
  "tool": "delete_database"
}

System Response:

Blocked: Invalid tool

Explanation:
The agent attempted to use an undefined tool. The system blocked execution using validation safeguards.

6. Safeguards Implemented
6.1 Tool Validation
Only predefined tools are allowed
Invalid tools are blocked
6.2 Controlled Tool Execution
Tools are executed only when required
No tool execution for approve/deny decisions
6.3 Input Validation
Missing attributes → request clarification
Prevents incorrect decisions
6.4 Single Tool Execution
Only one tool per request
Prevents conflicting actions
6.5 Loop Prevention
Single-step execution model
No recursive tool calls
Prevents infinite loops (e.g., repeated clarification)

7. Key Outcomes
The agent selects tools based on context and policy
High-risk actions are routed through approval workflows
Invalid or unsafe tool usage is blocked
The system ensures safe, auditable, and controlled automation

8. Summary

The agent demonstrates true agentic behavior by:

Making policy-driven decisions
Selecting appropriate tools
Executing actions safely
Preventing misuse through guardrails

The agent transitions from a reasoning system to a controlled execution system with built-in safety and compliance.
