import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MESH_API_KEY")
if not API_KEY:
    raise Exception("MESH_API_KEY missing from environment variables")

headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get("https://api.meshapi.ai/v1/models", headers=headers)

print(f"Status Code: {response.status_code}")

if response.status_code != 200:
    print("API Error Response:")
    print(response.text)
    exit()

data = response.json()

# Handle variations in response format
if isinstance(data, list):
    models = data
elif isinstance(data, dict) and "data" in data:
    models = data["data"]
else:
    print("Unexpected JSON structure:", data)
    exit()

print("\n" + "=" * 80)
print("AVAILABLE FREE MESH MODELS")
print("=" * 80)

free_models = []
for model in models:
    if model.get("is_free"):
        free_models.append(model)
        print("\nFREE MODEL")
        print("-" * 50)
        print("ID:", model.get("id"))
        print("Name:", model.get("name"))
        print("Provider:", model.get("brand"))
        print("Context:", model.get("context_length"))
        print(
            "Supports:",
            f"Tools: {model.get('supports_tools')} | "
            f"Structured Output: {model.get('supports_structured_output')} | "
            f"System Prompt: {model.get('supports_system_prompt')}"
        )

print("\n" + "=" * 80)
print(f"TOTAL FREE MODELS FOUND: {len(free_models)}")
print("=" * 80)