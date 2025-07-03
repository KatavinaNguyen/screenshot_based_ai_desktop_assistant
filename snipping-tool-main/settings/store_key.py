import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


# Encryption/Decryption Setup
def get_encryption_key():
    user_secret = "user-specific-salt"  # Replace for real apps
    return base64.urlsafe_b64encode(hashlib.sha256(user_secret.encode()).digest())

def encrypt_api_key(api_key):
    cipher = Fernet(get_encryption_key())
    return cipher.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key):
    cipher = Fernet(get_encryption_key())
    return cipher.decrypt(encrypted_key.encode()).decode()

# Load and Save Config
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config_data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

# Save user settings (model + key + correction mode)
def save_user_settings(model, api_key, correction_mode=False):
    config = load_config()

    if "api_keys" not in config:
        config["api_keys"] = {}

    # TEST: Save as plain text, then run production and comment-out this line, check config.json to see changes
    # config["api_keys"][model] = api_key

    # PRODUCTION: Save encrypted version
    config["api_keys"][model] = encrypt_api_key(api_key)

    config["selected_model"] = model
    config["correction_mode"] = correction_mode

    save_config(config)

# Load API key
def load_api_key(model):
    config = load_config()
    encrypted_key = config.get("api_keys", {}).get(model)
    if not encrypted_key:
        return None

    try:
        return decrypt_api_key(encrypted_key)
    except Exception as e:
        print(f"Decryption error: {e}")
        return None
