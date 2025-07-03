# test/test_pipeline.py

from capture.text_extract import extract_text_from_image
from generate.interpret import interpret_text
from generate.prompt import build_prompt
from send import response
import os

# Mock the real API call inside `send.response`
def mock_send_prompt(prompt_text: str, model: str = "chatgpt") -> str:
    print("\n[TEST] Prompt successfully passed to LLM dispatcher.")
    print(f"Model selected: {model}")
    print(f"Prompt sent:\n{prompt_text}\n")
    return "[TEST RESPONSE] This is a simulated reply. The pipeline works!"

# Replace real function with mock
response.send_prompt = mock_send_prompt


def test_pipeline_flow():
    print("Starting test pipeline...")

    project_root = os.path.dirname(os.path.dirname(__file__))
    image_path = os.path.join(project_root, "capture", "img", "eclip_ss.png")
    sample_text = ""

    # Try to extract text from real screenshot
    if os.path.exists(image_path):
        print(f"\nExtracting text from: {image_path}")
        sample_text = extract_text_from_image(image_path)
        print(f"\nExtracted text:\n{sample_text}")
    else:
        print("\nScreenshot image not found. Skipping OCR.")

    # Check if fallback is needed
    if not sample_text.strip():
        print("\nNo text extracted — using sample fallback text instead.")
        sample_text = """
        This Python function is throwing an error. Can you help me fix it?
        NameError: name 'my_variable' is not defined
        """

    # Step 1: Interpret the extracted or fallback text
    interpreted = interpret_text(sample_text)
    print(f"\nInterpreted Data:\n{interpreted}")

    # Step 2: Build prompt
    prompt = build_prompt(interpreted)
    print(f"\nFinal Prompt:\n{prompt}")

    # Step 3: Send prompt (mocked)
    reply = response.send_prompt(prompt)
    print(f"\nSimulated LLM Reply:\n{reply}")


if __name__ == "__main__":
    test_pipeline_flow()
