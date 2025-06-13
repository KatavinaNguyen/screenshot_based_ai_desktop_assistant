import openai
from settings import config, store_key
from generate.prompt import build_prompt

def send_to_chatgpt(extracted_text: str) -> str:
    cfg = config.load_config()
    correction_mode = cfg.get("correction_mode", False)
    prompt = build_prompt(extracted_text, correction_mode)

    api_key = store_key.load_api_key("ChatGPT")  # Load and decrypt
    if not api_key:
        return "⚠️ API key not found."

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=100
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ API call failed: {e}"
