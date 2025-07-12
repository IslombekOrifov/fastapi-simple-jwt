# 🛡️ fastapi-simple-jwt

**Advanced JWT Authentication Library** for FastAPI with refresh tokens, multiple device support, token blacklisting, and flexible configuration – inspired by Django Simple JWT.

---


## ⚙️ Configuration

1. Create your Config class in your project (e.g. app/config.py):


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
FASTAPI_AUTH_CONFIG=app.config.Config
```

## 🛠️ Database Migration

Your project's Alembic configuration already includes your Base.

Since `fastapi-advanced-jwt` uses your configured `Base` from `Config.BASE`, simply run:

```bash
alembic revision --autogenerate -m "Add RefreshToken table"
alembic upgrade head


## 🚀 Usage

Add routers in your main.py:
```bash
from fastapi import FastAPI
from fastapi_simple_jwt.routers import router

app = FastAPI()

# Add JWT routers
app.include_router(router)

```

in fronend you should add fingerprint too:
```
<script src="https://openfpcdn.io/fingerprintjs/v3"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/clientjs/0.1.11/client.min.js"></script>

<script>
  async function getFingerprint() {
    const fp = await FingerprintJS.load();
    const result = await fp.get();
    const client = new ClientJS();

    const advanced_fp = {
      visitorId: result.visitorId,
      userAgent: client.getUserAgent(),
      os: client.getOS(),
      osVersion: client.getOSVersion(),
      browser: client.getBrowser(),
      browserVersion: client.getBrowserVersion(),
      screenPrint: client.getScreenPrint(),
      timezone: client.getTimeZone(),
      language: client.getLanguage(),
      cpu: client.getCPU(),
      plugins: client.getPlugins(),
      fonts: client.getFonts(),
      canvasPrint: client.getCanvasPrint(),
      deviceMemory: navigator.deviceMemory || "unknown",
      hardwareConcurrency: navigator.hardwareConcurrency || "unknown",
    };

    return advanced_fp;
  }

  async function login() {
    const fingerprint = await getFingerprint();
    const response = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: "test@example.com",
        password: "password",
        fingerprint: fingerprint
      })
    });
    const data = await response.json();
    console.log(data);
  }
</script>
```

## Don't forget add text about saved datas with hashed fingerprint to your Privacy&Policy in your site!

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