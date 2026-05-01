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

Conversation1

User: QA requests write access to production DB

Agent:
- Identifies role = QA, resource = production DB
- Checks policy → QA allowed read-only access
- Evaluates risk → production + write = high risk
- Decision → deny or escalate

Output:
Decision: requires_approval  
Reason: Write access to production DB is restricted and requires approval  
Next Step: Do you want me to raise approval request?

Conversation2 (HITL Escalation):

User: User logged in from India and US within 1 hour

Agent:
- Fetches login history
- Detects geo-velocity anomaly
- Assigns risk = high
- Decision → escalate

Output:
Decision: escalate_to_SecOps  
Reason: Suspicious login behaviour detected  
Next Step: Initiate incident response?

**What makes it “industry-grade” (and not a toy)**

- Role-based (RBAC) and attribute-based (ABAC) access evaluation
- Risk-based decision making using contextual signals
- Policy traceability (explicit rule references in decisions)
- Explainable outputs for audit and compliance
- Human-in-the-loop enforcement for sensitive actions
- Structured escalation workflows
- Separation of decision logic and policy data (extensible design)


