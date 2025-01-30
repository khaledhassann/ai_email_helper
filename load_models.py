import ollama

# Define the locally installed Ollama model
OLLAMA_MODEL = "deepseek-r1:7b-qwen-distill-q4_K_M"

def generate_response(prompt: str):
    """
    Call Ollama's local model and return the generated response.
    """
    response = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
