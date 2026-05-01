def classify_request(user_input):
    user_input = user_input.lower()
    if "access" in user_input:
        return "access_request"
    elif "login" in user_input or "location" in user_input:
        return "anamoly_detection"
    else:
        return "unknown"
    
def handle_access_request(user_input):
    if "qa" in user_input and "write" in user_input and "production" in user_input:
        return {
            "decision" :"deny",
            "reason" : "QA cannot have write access to production"
        }
    elif "read" in user_input and "test" in user_input:
        return {
            "decision":"approve",
            "reason" : "tester can have read access to test db"
        }
    else:
        return {
            "decision":"escalate",
            "reason": "insufficient information"
        }
    
def handle_anamoly(user_input):
    if "india" in user_input and "us" in user_input:
        return {
            "decision": "flag",
            "reason": "Multiple locations detected"
        }
    else:
        return {
            "decision": "normal",
            "reason":"no anamoly detected"
        }
    
def agent_response(user_input):
    request_type = classify_request(user_input)

    if request_type == "access_request":
        return handle_access_request(user_input)
    elif request_type == "anamoly_detection":
        return handle_anamoly(user_input)
    else:
        return {
            "decision": "unknown",
            "reason": "Could not understand request"
        }

if __name__ == "__main__":
    print("IAM BASELINE AGENT(RULE-BASED)")
    while True:
        user_input = input("\nEnter your request:")
        if user_input.lower() == "exit":
            break
        response = agent_response(user_input)

        print("\nResponse:")
        for k,v in response.items():
            print(f"{k}:{v}")
    # Logging
        with open("./logs/baseline_logs.txt", "a") as log:
            log.write(f"Input: {user_input}\n")
            log.write(f"Output: {response}\n\n")
