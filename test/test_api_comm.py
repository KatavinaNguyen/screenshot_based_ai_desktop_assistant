from generate.prompt import build_prompt
from send.response import dispatch_prompt

extracted_text = "Explain Newton's Second Law of Motion"
correction_mode = False
selected_model = "chatgpt"

prompt = build_prompt(extracted_text, correction_mode=correction_mode)
response = dispatch_prompt(prompt, model=selected_model)
print(response)
