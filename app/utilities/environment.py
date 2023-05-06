import os
from pathlib import Path


class Environment(object):
    ENV_VAR_KEY_ENV = "ENV"
    _ENV_VAR_PRODUCTION = ("production", "prod")

    @staticmethod
    def get(key):
        if key in os.environ:
            return os.environ[key]
        return None

    @staticmethod
    def is_production():
        if Environment.ENV_VAR_KEY_ENV in os.environ:
            env = os.environ[Environment.ENV_VAR_KEY_ENV]
            return env is not None and env.lower() in Environment._ENV_VAR_PRODUCTION

        return False

    @staticmethod
    def config_path():
        cwd = Path.cwd()
        config_variant = os.environ.get("CONFIG_VARIANT")
        env = "production" if Environment.is_production() else "development"
        config_file = (
            f"config-{env}-{config_variant}.json" if config_variant else f"config-{env}.json"
        )
        config_path = cwd / "config" / config_file

        if not config_path.exists():
            raise Exception(f"Config `{config_path}` NOT found")

        return config_path
