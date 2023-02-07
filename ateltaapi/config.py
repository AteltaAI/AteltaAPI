import os

from dynaconf import Dynaconf

HERE = os.path.dirname(os.path.abspath(__file__))

settings = Dynaconf(
    envvar_prefix="ateltaapi",
    preload=[os.path.join(HERE, "default.toml")],
    settings_files=["settings.toml", ".secrets.toml"],
    environments=["development", "production", "testing"],
    env_switcher="ateltaapi_env",
    load_dotenv=False,
)


"""
# How to use this application settings

```
from ateltaapi.config import settings
```

## Acessing variables

```
settings.get("SECRET_KEY", default="sdnfjbnfsdf")
settings["SECRET_KEY"]
settings.SECRET_KEY
settings.db.uri
settings["db"]["uri"]
settings["db.uri"]
settings.DB__uri
```

## Modifying variables

### On files

settings.toml
```
[development]
KEY=value
```

### As environment variables
```
export ateltaapi_KEY=value
export ateltaapi_KEY="@int 42"
export ateltaapi_KEY="@jinja {{ this.db.uri }}"
export ateltaapi_DB__uri="@jinja {{ this.db.uri | replace('db', 'data') }}"
```

### Switching environments
```
ateltaapi_ENV=production ateltaapi run
```

Read more on https://dynaconf.com
"""
