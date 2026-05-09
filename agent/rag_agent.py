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

ACCESS RULES:
- If role NOT in allowed_roles → DENY
- If access_type not permitted → DENY
- If conditions include approval_required → ESCALATE
- If resource is high-risk → prefer ESCALATION

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

------------------------
OUTPUT FORMAT (STRICT JSON):

{{
  "request_type": "",
  "decision": "",
  "reason": "",
  "risk": "",
  "next_step": ""
}}

------------------------
IMPORTANT RULES:

- Do NOT hallucinate policies
- If no matching policy → return decision = "unknown"
- Always include reasoning based on policy
- Keep response concise and structured
"""

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
    return json.loads(response.content)


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
