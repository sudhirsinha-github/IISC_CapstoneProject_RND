import json
from sklearn.model_selection import train_test_split

# Load uploaded dataset
file_path = "/mnt/data/labeled_2025-06-28.jsonl"
with open(file_path, "r", encoding="utf-8") as f:
    full_data = [json.loads(line) for line in f]

# Split 80/20
train_data, eval_data = train_test_split(full_data, test_size=0.2, random_state=42)

# Convert to instruction format
def to_prompt(example):
    user_input = example["messages"][0]["content"]
    structured_output = {
        "intent": example["intent"][0],
        "sentiment": example["sentiment"][0],
        "topic": example["topic"][0],
        "entities": example["entities"]
    }
    prompt = (
        f"Classify the following:\n{user_input}\n"
        f"Return JSON: {json.dumps(structured_output)}"
    )
    return {"prompt": prompt}

# Apply transformation
train_formatted = [to_prompt(x) for x in train_data]
eval_formatted = [to_prompt(x) for x in eval_data]

# Save to JSONL files
train_out = "/mnt/data/train_phi2.jsonl"
eval_out = "/mnt/data/eval_phi2.jsonl"

with open(train_out, "w", encoding="utf-8") as f:
    for ex in train_formatted:
        f.write(json.dumps(ex) + "\n")

with open(eval_out, "w", encoding="utf-8") as f:
    for ex in eval_formatted:
        f.write(json.dumps(ex) + "\n")

(train_out, eval_out)
