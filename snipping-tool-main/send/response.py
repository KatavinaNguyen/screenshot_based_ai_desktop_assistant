from send.llm_clients import ask_chatgpt
from send.llm_clients import ask_claude
from send.llm_clients import ask_gemini

def dispatch_prompt(prompt: str, model: str = "chatgpt") -> str:
    """
    Dispatch the prompt to the selected AI model.
    :param prompt: Formatted prompt string.
    :param model: Target model name (chatgpt, claude, gemini).
    :return: AI model's response or error string.
    """
    if model == "chatgpt":
        return ask_chatgpt.send_prompt_to_chatgpt(prompt)
    elif model == "claude":
        return ask_chatgpt.send_prompt_to_claude(prompt)
    elif model == "gemini":
        return ask_chatgpt.send_prompt_to_gemini(prompt)
    else:
        return "❌ Invalid model selected."


# add custom = True later on for (open browser + paste prompt)
