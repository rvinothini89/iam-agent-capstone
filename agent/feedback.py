import json
import os

FEEDBACK_FILE = "data/feedback.json"

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    return []

def save_feedback(feedback):
    data = load_feedback()
    data.append(feedback)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data,f,indent = 2)
