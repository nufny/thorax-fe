import tomllib


def get_settings() -> dict[str, str]:
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    return config
