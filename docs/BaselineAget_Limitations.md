**Limitations of Baseline Agent**

The baseline agent is implemented using simple keyword-based rules and lacks the ability to perform contextual reasoning, dynamic decision-making, and multi-turn understanding. The following limitations were observed:

**Limited Natural Language Understanding**

The agent relies on keyword matching for classification, which makes it incapable of handling variations in user input.

Example: 
Input: User logged in from India and US within 1 hour  
Output: {'decision': 'unknown', 'reason': 'Could not understand request'}

Issue:
The agent fails to detect anomaly because it depends on specific keywords (e.g., "login") and cannot interpret semantically similar inputs.

**Static Rule-Based Decision Making**

The agent follows predefined rules and cannot adapt decisions based on context, urgency, or justification.

Example: 
Input: I urgently need elevated access to production db for hotfix
Output: {'decision': 'escalate', 'reason': 'insufficient information'} 

Issue:
Even though the request may be valid, the agent cannot evaluate intent, urgency, or business context, leading to incorrect or incomplete decisions.

**No Context Awareness (Lack of Memory)**

The agent processes each input independently and cannot retain or use information from previous interactions.

Example:
Input 1: I urgently need elevated access to production db for hotfix  
Output: {'decision': 'escalate', 'reason': 'Insufficient information'}

Input 2: Hotfix is in two days and this request needs to be handled ASAP  
Output: {'decision': 'unknown', 'reason': 'Could not understand request'}

Issue:
The agent fails to connect related inputs and cannot build context across multiple turns, resulting in poor conversational handling.
