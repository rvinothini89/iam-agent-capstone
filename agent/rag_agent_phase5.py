from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from rag.retriever import get_relevant_docs
from dotenv import load_dotenv
import json
import os

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

PROMPT_RAG = """
You are an IAM (Identity and Access Management) security agent.

You are responsible for evaluating:
1. Access requests
2. Anomalous user behavior

You MUST use the provided policy context strictly. Do not make assumptions outside it.

------------------------
POLICY CONTEXT:
{context}
------------------------

USER INPUT:
{input}

------------------------
INSTRUCTIONS:

Step 1: Identify request type
- access_request OR anomaly_detection

Step 2: Extract key attributes
- role (QA, DevOps, Admin, etc.)
- resource (production_db, test_db, etc.)
- access type (read, write, full_access)
- any conditions (urgency, time, location)

------------------------
MISSING INFORMATION HANDLING (HIGH PRIORITY):

- If role is missing → DO NOT evaluate policies
- If access type is unclear → DO NOT evaluate policies
- If required attributes are missing → return "request_clarification"

In such cases:
- decision = "request_clarification"
- risk = "unknown"
- next_step = ask user for missing details

Step 3: Evaluate against policies

PRIORITY RULE:
Missing information handling takes precedence over all other rules.
Do NOT evaluate policies if required attributes are missing.

Step 4: Assign risk level

- If resource is production_db or marked as high-risk → risk = high
- If access_type is write or full_access on sensitive resource → risk = high
- If approval_required → risk = at least medium
- Otherwise assign low / medium based on policy

ACCESS RULES:

- If role NOT in allowed_roles:
    - If resource is high-risk (e.g., production_db) → ESCALATE
    - Otherwise → DENY

- If access_type not permitted:
    - If approval_required OR resource is high-risk → ESCALATE
    - Otherwise → DENY

- If conditions include approval_required → ESCALATE

- If resource is high-risk → prefer ESCALATION

HIGH-RISK RULE:

- Production systems (e.g., production_db) are always considered high-risk
- Any write or elevated access to such systems must be treated as high risk

ANOMALY RULES:
- If behavior matches anomaly_policies (e.g., geo_velocity) → ESCALATE to SecOps
- Assign risk based on policy

APPROVAL RULES:
- If approval required → escalate to:
  - Incident Manager (for high risk)
  - Manager (for production write)

Step 4: Assign risk level
- low / medium / high (based on policy)

------------------------
DECISION LOGIC:

Return ONLY one of:
- approve
- deny
- escalate
- request_clarification

------------------------
AVAILABLE TOOLS:

1. request_approval(resource, role, access_type)
   - Use when access requires approval (e.g., production write, high-risk)

2. escalate_to_secops(issue)
   - Use when anomaly or suspicious activity is detected

3. ask_user_details(missing_fields)
   - Use when required input information is missing

------------------------
TOOL USAGE RULES:

- If decision = escalate (access request) → use request_approval
- If anomaly detected → use escalate_to_secops
- If decision = request_clarification → use ask_user_details
- If decision = approve or deny → do NOT call any tool

- Always provide tool_input with required parameters
- Do NOT call multiple tools
- Do NOT call tool if not required

NEXT STEP RULES:

- If a tool is executed, next_step should describe the completed action
- Do NOT suggest future action if tool_result already performed it
- Example:
    - If request_approval tool is used → "Approval request has been sent to Manager"
    - If escalate_to_secops is used → "Incident has been escalated to SecOps"
    - If ask_user_details is used → "Waiting for user to provide missing details"

------------------------
OUTPUT FORMAT (STRICT JSON):

{{  
  "request_type": "",
  "decision": "",
  "reason": "",
  "risk": "",
  "tool": "",
  "tool_input": {{}},
  "next_step": ""
}}

------------------------
IMPORTANT RULES:

- Do NOT hallucinate policies
- If no matching policy → return decision = "unknown"
- Always include reasoning based on policy
- Keep response concise and structured

POLICY TRACEABILITY RULE:

- Always reference the relevant policy in the reason field when available
- Include policy ID or rule (e.g., "as per policy P2")
- Do NOT invent policy IDs — only use those present in context

SAFETY AND COMPLIANCE RULE:

- For high-risk or privileged access, explicitly mention that human approval is required
- Clearly indicate that the action is not automatically executed
- Ensure decisions follow least-privilege and security best practices

REASONING RULE:

- The reason must include:
    1. Policy reference (if available)
    2. Risk justification (why it is high/medium/low)
    3. Action justification (why escalate/deny/approve)

- Always mention if the resource is high-risk (e.g., production systems)
"""

def request_approval(resource, role, access_type):
    return f"Approval request created for {role} to get {access_type} access on {resource}"

def escalate_to_secops(issue):
    return f"Security incident escalated to SecOps: {issue}"

def ask_user_details(missing_fields):
    return f"Please provide the following details: {missing_fields}"

TOOLS = [
    {
        "name": "request_approval",
        "description": "Use when access requires approval",
        "parameters": ["resource", "role", "access_type"]
    },
    {
        "name": "escalate_to_secops",
        "description": "Use when anomaly or security issue detected",
        "parameters": ["issue"]
    },
    {
        "name": "ask_user_details",
        "description": "Use when input is missing required information",
        "parameters": ["missing_fields"]
    }
]

def parse_response(content: str):
    content = content.strip()

    # Remove markdown formatting if present
    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "decision": "error",
            "reason": "Failed to parse LLM response",
            "raw_output": content
        }

def execute_tool(tool_name, tool_input):
    if tool_name == "request_approval":
        return request_approval(**tool_input)
    elif tool_name == "escalate_to_secops":
        return escalate_to_secops(**tool_input)
    elif tool_name == "ask_user_details":
        return ask_user_details(**tool_input)
    else:
        return "Invalid tool"

def run_rag_agent(user_input):
    docs = get_relevant_docs(user_input)

    if not docs:
        return {
            "decision": "unknown",
            "reason": "No relevant policy found",
            "risk": "unknown"
        }

    context = "\n\n".join(docs)

    prompt = PromptTemplate(
        input_variables=["context", "input"],
        template=PROMPT_RAG
    )

    formatted = prompt.format(context=context, input=user_input)

    response = llm.invoke(formatted)
    parsed = parse_response(response.content)

    VALID_TOOLS = ["request_approval", "escalate_to_secops", "ask_user_details"]

    if parsed.get("tool"):
        tool_input = parsed.get("tool_input") or {}

        if parsed["tool"] not in VALID_TOOLS:
            parsed["tool_result"] = "Blocked: Invalid tool"
        else:
            try:
                parsed["tool_result"] = execute_tool(parsed["tool"], tool_input)
            except Exception as e:
                parsed["tool_result"] = f"Tool execution failed: {str(e)}"

    return parsed

if __name__ == "__main__":
    print("IAM RAG Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("Enter request: ")

        if user_input.lower() == "exit":
            print("Exiting agent...")
            break

        response = run_rag_agent(user_input)

        print("\nResponse:")
        print(json.dumps(response, indent=2))
        print("\n----------------------")
