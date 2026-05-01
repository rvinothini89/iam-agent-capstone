**Problem Statement:**

In modern organizations, access requests to systems and resources (e.g., databases, admin consoles, shared drives) are frequent and critical. These requests must be evaluated based on multiple factors such as user role, tenure, security clearance, resource sensitivity, and contextual risk signals.
Currently, L1 or IAM support teams manually review requests, gather missing details, consult policy documents, and decide whether to approve, deny, or escalate. This process is slow, inconsistent, and prone to human error. Additionally, anomalous access patterns (e.g., unusual login locations or times) often go unnoticed or are handled reactively. There is a need for an intelligent agent that can interpret access requests, evaluate them against policies, detect anomalies, and provide safe, explainable decisions while enforcing approval workflows for sensitive actions.

**Additional Scenario: Anomaly Detection**

The agent should also detect anomalous access behaviour such as:
- Login from multiple geographic locations in a short time
- Access outside business hours
- Access from unknown devices

The agent should classify risk levels and take appropriate actions such as flagging, escalation, or account restriction.

**Primary Goal:**

The goal of the agent is to evaluate access requests and detect anomalous access behaviour by applying IAM policies, contextual risk signals, and user attributes. The agent should provide clear decisions (approve, deny, escalate), explain its reasoning, and enforce human-in-the-loop approval for sensitive or high-risk actions while ensuring compliance and consistency.

**Scope And Boundaries**

Allowed Actions

- Classify request type (access request / anomaly detection)
- Extract relevant attributes (role, resource, access type)
- Retrieve IAM policies and rules
- Evaluate access based on policy + context
- Detect anomalous behaviour using activity logs
- Provide decision with reasoning (approve/deny/escalate)
- Generate approval or escalation notes

Inputs and Outputs

Inputs:
- User access request (natural language)
- User attributes (role, department, tenure)
- IAM policies
- Activity logs (login history, device, location)

Outputs:
- Decision (approve / deny / escalate)
- Reasoning (policy + risk explanation)
- Confidence level (optional)
- Next action (approval request / escalation / clarification)

Success Criteria

- Decision Accuracy: ≥ 80% correct decisions across test scenarios
- Policy Compliance: No violation of defined IAM policies
- Explainability: Each response includes reasoning and policy reference
- Safety: Agent refuses unsafe or unauthorized actions
- Escalation Accuracy: High-risk cases are correctly escalated
- Anomaly Detection Accuracy: Correct identification of anomalous vs normal behaviour

**Human-in-the-Loop (HITL) Involvement**

The agent must involve a human decision-maker in the following scenarios:

1. Privileged or High-Risk Access Requests
- Example: Write or admin access to production systems
- Action: Do not approve directly; generate an approval request for the appropriate authority (e.g., Manager / SecOps)

2. Policy Conflicts or Ambiguity
- When multiple policies apply or the decision is unclear
- Action: Escalate with a summary of conflicting rules and request human review

3. Low Confidence Decisions
- When the agent cannot confidently classify or evaluate the request
- Action: Ask for additional information or escalate for manual validation

4. Anomalous or Suspicious Behaviour
- Example: Login from multiple locations within a short time
- Action: Escalate to SecOps and request confirmation before taking further action

5. Sensitive Security Context
- Example: Potential compromised account or unusual activity
- Action: Immediately escalate and avoid automated decisions

HITL Interaction Format:
“This request requires approval due to policy restrictions or risk level. Would you like me to generate an approval request or escalate to the appropriate team? (yes/no)”

Assumptions

- IAM policies are accurate and up-to-date
- User attributes are reliably available
- Logs are sufficient for anomaly detection
- Agent decisions are advisory and subject to approval where required

**Out of scope **

Performing privileged system actions without approval
Bypassing authentication/access control
Final security incident resolution without SecOps

**User Types**
End user (requester), L1 agent (operator), L2/L3 engineer, Incident manager, Security team (SecOps)

**Formal Conversation Sample **

Conversation1 - Routine Access Request (End User + Agent)

User (End User):
I need read access to test database for debugging.

Agent:
- Identifies role = QA
- Resource = test_db
- Checks policy → QA allowed read access
- Risk = low

Output:
Decision: approve  
Reason: QA role is permitted read access to test database  
Next Step: Access can be provisioned automatically

Conversation2 - Privileged Access (Agent + Manager / L2)

User:
I need write access to production DB for urgent fix.

Agent:
- Identifies role = QA
- Checks policy → write access restricted
- Risk = high

Agent:
This request requires approval due to high-risk access.
Do you want me to raise an approval request? (yes/no)

User:
Yes

Agent → L2/Manager:
Approval Request:
- User: QA
- Resource: production DB
- Access: write
- Reason: urgent fix
- Risk: high

L2/Manager:
Approved for 4 hours with audit logging

Agent:
Decision: approved_with_conditions  
Conditions: time-limited access (4 hours), audit logging enabled

Conversation 3 — Anomaly Detection (Agent + SecOps)

System Input:
User logged in from India and US within 1 hour

Agent:
- Fetches logs
- Detects geo-velocity anomaly
- Risk = high

Agent:
Decision: escalate_to_SecOps  
Reason: Suspicious login behaviour detected

Agent → SecOps:
Incident Summary:
- User: Vinothini
- Activity: Multiple geo-locations within 1 hour
- Risk: High

SecOps:
Initiate account lock and investigation

Agent:
Action: Account temporarily locked and incident escalated

Conversation 4 — Access Review (Agent + Incident Manager)

System Input:
User inactive for 120 days but has admin access to production systems

Agent:
- Checks user activity → last login = 120 days
- Identifies role = Admin (high privilege)
- Applies review policy → inactive > 90 days → review required

Agent:
Decision: review_required  
Reason: High privilege access with prolonged inactivity  

Agent → L2/L3 Engineer:
Technical Validation Request:
- User: Vinothini
- Role: Admin
- Last activity: 120 days ago
- Resource: production systems

Question:
Is this access still required for any ongoing tasks or system dependencies?

L2/L3 Engineer:
- Confirms no active tasks assigned to the user
- Confirms no system dependency on this account

Response:
Access is no longer required from a technical standpoint.

Agent → Incident Manager:
Access Review Summary:
- User inactive for 120 days
- Role: Admin
- L2/L3 validation: No active dependency
- Recommendation: Remove access

Incident Manager:
Approved removal

Agent:
Final Decision: remove_access  
Action: Access marked for deprovisioning

**What makes it “industry-grade” (and not a toy)**

- Role-based (RBAC) and attribute-based (ABAC) access evaluation
- Risk-based decision making using contextual signals
- Policy traceability (explicit rule references in decisions)
- Explainable outputs for audit and compliance
- Human-in-the-loop enforcement for sensitive actions
- Structured escalation workflows
- Separation of decision logic and policy data (extensible design)


