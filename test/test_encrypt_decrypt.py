"""
TEST:
To check if its encrypting and decrypting properly
reminder: after testing, delete the config.json to reset. (it'll say you have an api key saved in the menu if you don't)

can use this to reset the config.json to test whether your keys are saving correctly
just remember to reset the config.json file once you're done testing or else it will
say that it has a key saved but that's not an actual key

This test verifies that the API key encryption and decryption system is working correctly.
It checks whether API keys for different models (ChatGPT, Claude, Gemini) are properly:
- Encrypted when saved
- Decrypted when loaded
- Matched against the original key values

PASS:
Saving API key for ChatGPT...
Settings saved for ChatGPT. Correction mode: False
Saving API key for Claude...
Settings saved for Claude. Correction mode: False
Saving API key for Gemini...
Settings saved for Gemini. Correction mode: False

Verifying API key decryption:
ChatGPT: Match | Loaded: sk-chatgpt-test-key-123
Claude: Match | Loaded: sk-claude-test-key-456
Gemini: Match | Loaded: sk-gemini-test-key-789

Current config.json content:
selected_model: Gemini
correction_mode: False
api_keys: {'ChatGPT': '...=', 'Claude': '...=', 'Gemini': '...='} (... is encrypted api key)
"""

from settings import store_key, config

# Test values
test_keys = {
    "ChatGPT": "sk-chatgpt-test-key-123",
    "Claude": "sk-claude-test-key-456",
    "Gemini": "sk-gemini-test-key-789"
}

# Save all test keys
for model, key in test_keys.items():
    print(f"Saving API key for {model}...")
    store_key.save_user_settings(model, key)

# Load and verify all test keys
print("\nVerifying API key decryption:")
for model, original_key in test_keys.items():
    loaded_key = store_key.load_api_key(model)
    status = "Match" if loaded_key == original_key else "Mismatch"
    print(f"{model}: {status} | Loaded: {loaded_key}")

# Show current config.json content
print("\nCurrent config.json content:")
current_config = config.load_config()
for k, v in current_config.items():
    print(f"{k}: {v}")
