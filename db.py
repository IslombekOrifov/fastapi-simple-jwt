from .settings import get_auth_config


Config = get_auth_config()

Base = Config.BASE
get_session = Config.GET_SESSION


