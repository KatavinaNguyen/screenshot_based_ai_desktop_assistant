from .store_key import load_config, load_api_key

def get_selected_model():
    config = load_config()
    return config.get("selected_model", "chatgpt")  # default fallback

def get_correction_mode():
    config = load_config()
    return config.get("correction_mode", False)

def get_api_key(model=None):
    from .store_key import load_api_key
    model = model or get_selected_model()
    return load_api_key(model)
