Phase 5: Tool Usage (Agentic Capabilities)
Overview

In this phase, the IAM agent is enhanced to select and execute tools based on its decisions. The agent now moves beyond reasoning and retrieval to taking controlled actions, while enforcing safeguards to prevent misuse.

1. Tools Defined

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

Output:

{
  "decision": "escalate",
  "tool": "request_approval",
  "reason": "QA is not permitted write access as per policy P2. Production DB is high-risk and requires approval.",
  "tool_result": "Approval request created..."
}
Example 2: Low-Risk Access Request

Input:
Need read access to test database

Output:

{
  "decision": "approve",
  "tool": ""
}

✔ No tool invoked for safe operations

Example 3: Missing Information

Input:
I need access

Output:

{
  "decision": "request_clarification",
  "tool": "ask_user_details"
}
Example 4: Anomaly Detection

Input:
User logged in from India and US within 1 hour

Output:

{
  "decision": "escalate",
  "tool": "escalate_to_secops"
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
