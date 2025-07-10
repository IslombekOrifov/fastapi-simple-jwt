# 🛡️ fastapi-simple-jwt

**Advanced JWT Authentication Library** for FastAPI with refresh tokens, multiple device support, token blacklisting, and flexible configuration – inspired by Django Simple JWT.

---

## 📦 Installation

```bash
pip install fastapi-advanced-jwt
```

## ⚙️ Configuration

1. Create your AuthConfig class in your project (e.g. app/config.py):


```
from datetime import timedelta

class Config:
    # *** 
    SECRET_KEY = "supersecretkey"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
    REFRESH_TOKEN_LIFETIME = timedelta(days=7)
    
    USER_MODEL = "app.models.User"
    USERNAME_FIELD = "email"
    PASSWORD_FIELD = "hashed_password"
    PASSWORD_SCHEMES = ['bcrypt']
    
    # Database
    BASE = Base #(your class)
    GET_SESSION = get_session  #(your session func)
    
    # Options
    BLACKLIST_ENABLED = True
    ROTATE_REFRESH_TOKENS = True
    BLACKLIST_STRATEGY = "BLACKLIST_REFRESH"  # or "BLACKLIST_BOTH"
    MAX_DEVICES_PER_USER = 3
```

2. Set environment variable in your .env file::

```bash
FASTAPI_AUTH_CONFIG=app.config.AuthConfig
```


## 🚀 Usage

Add routers in your main.py:
```bash
from fastapi import FastAPI
from fastapi_simple_jwt.routers import router

app = FastAPI()

# Add JWT routers
app.include_router(router)

```

## 📲 Endpoints

| Method | Path                    | Description                                               |
| ------ | ----------------------- | --------------------------------------------------------- |
| POST   | `/login`                | Login with username/password, get access + refresh tokens |
| POST   | `/refresh`              | Refresh tokens (rotation supported)                       |
| POST   | `/logout`               | Revoke current refresh token                              |
| POST   | `/logout_all`           | Revoke all sessions for user                              |
| GET    | `/active_sessions`      | List active tokens/sessions                              |
| POST   | `/revoke_other_session` | Revoke other sessions except current                      |



## 🔐 Features

✅ Access + Refresh token system
✅ Multiple device sessions
✅ Token rotation
✅ Blacklist support (refresh / both)
✅ Middleware for revoked access tokens
✅ Config-driven (like Django settings)
✅ Clean async SQLAlchemy architecture


---