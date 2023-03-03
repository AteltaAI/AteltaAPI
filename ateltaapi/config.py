import os
from dynaconf import Dynaconf

# TBD
# TODO:
# - Create settings.toml
# - Create .secrets.toml for storing secrets

HERE = os.path.dirname(os.path.abspath(__file__))
settings = Dynaconf(envvar_prefix="ateltaapi")
