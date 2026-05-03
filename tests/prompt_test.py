from agent.llm_agent import run_prompt
from agent.prompts import PROMPT_1, PROMPT_2, PROMPT_3

test_inputs = [
    "QA needs write access to production DB",
    "Need read access to test database",
    "User logged in from India and US within 1 hour",
    "I urgently need elevated access to production db for hotfix"
]

results = []

for input_text in test_inputs:
    print("\n==============================")
    print(f"Input: {input_text}")

    output1 = run_prompt(PROMPT_1, input_text)
    output2 = run_prompt(PROMPT_2, input_text)
    output3 = run_prompt(PROMPT_3, input_text)

    print("\nPrompt 1 Output:\n", output1)
    print("\nPrompt 2 Output:\n", output2)
    print("\nPrompt 3 Output:\n", output3)

    results.append({
        "input": input_text,
        "p1": output1,
        "p2": output2,
        "p3": output3
    })

# Save results
with open("./outputs/comparison_results.txt", "w") as f:
    for r in results:
        f.write(f"Input: {r['input']}\n")
        f.write(f"P1: {r['p1']}\n")
        f.write(f"P2: {r['p2']}\n")
        f.write(f"P3: {r['p3']}\n")
        f.write("\n----------------------\n")
