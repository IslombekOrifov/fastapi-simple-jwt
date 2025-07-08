import importlib
import os

_auth_config = None

def get_auth_config():
    global _auth_config
    if _auth_config is None:
        config_path = os.getenv("FASTAPI_AUTH_CONFIG")
        if config_path is None:
            raise ImportError("Set FASTAPI_AUTH_CONFIG env variable to your AuthConfig path, e.g. 'app.config.AuthConfig'")
        module_name, class_name = config_path.split('.', 1)
        module = importlib.import_module(module_name)
        _auth_config = getattr(module, class_name)
    return _auth_config
        