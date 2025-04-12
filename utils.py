import json
import re

def load_json(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def dump_json(file, path):
    with open(path, 'w') as json_file:
        json.dump(file, json_file, indent=4)

def load_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def dump_text(file, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(file)

def call_llm(client, message, model='deepseek-chat', temperature=0):
    
    response = client.chat.completions.create(
        model=model,
        messages=message,
        temperature=temperature,
        stream=False
    )

    try:
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling LLM: {str(e)}"
    
def extract_json_block(text: str) -> dict:
    """
    Extract and parse JSON from a string, even if it's wrapped in markdown code block like ```json ... ```.
    """
    # Step 1: Extract JSON content between triple backticks if they exist
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        json_str = text.strip()
    
    # Step 2: Parse JSON
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON content: {e}")