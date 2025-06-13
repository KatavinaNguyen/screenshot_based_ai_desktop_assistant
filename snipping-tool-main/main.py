from capture.text_extract import extract_text_from_image
from generate.prompt import build_prompt

image_path = "capture/img/eclip_ss.png"
extracted_text = extract_text_from_image(image_path)
interpreted = interpret_text(extracted_text)
prompt = build_prompt(interpreted)
response = send_prompt(prompt)  # ChatGPT used by default

print("\n🧠 LLM Response:\n", response)
