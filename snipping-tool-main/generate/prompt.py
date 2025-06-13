def build_prompt(extracted_text: str, correction_mode: bool = False) -> str:
    """
    Build the appropriate prompt based on whether correction mode is active.

    :param extracted_text: The text extracted from the screenshot.
    :param correction_mode: Boolean flag for correction mode.
    :return: Formatted prompt string.
    """

    if correction_mode:
        prompt = f"""You are a text correction assistant.
        Your task is to return a corrected version of the text.
        If unclear, resolve meaning in the most logical and helpful way.
        Text:
        \"\"\"
        {extracted_text}
        \"\"\""""
    else:
        prompt = f"""You are an answer-only desktop assistant.
        Your task is to Process of elimination:
        [1] If none apply, say 'None'
        [2] Answer directly with minimal words. If unclear or error-related, give brief user steps.
        [3] Rephrase in simple terms to preserve intent, completely cut ambiguity, pay attention to numbers, bullets when useful. max_tokens=50
        [4] Briefly explain a standalone concept with a short example when helpful.
        Text:
        \"\"\"
        {extracted_text}
        \"\"\""""

    return prompt
