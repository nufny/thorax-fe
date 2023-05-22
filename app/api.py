import json

import httpx

from app.models import Config
from app.settings import get_settings

settings = get_settings()
config_url = f"https://{settings['host']}/api/v1/pleroma/admin/config"
auth_header = {"Authorization": f"Bearer {settings['token']}"}


def get_config() -> Config:
    response = httpx.get(config_url, headers=auth_header)
    assert response.status_code == 200, f"{response.status_code}: {response.json()}"
    configs = response.json()["configs"]
    return Config.from_dict(configs)


def update_configs(config: Config) -> httpx.Response:
    headers = auth_header | {
        "Content-Type": "application/json;charset=utf-8",
    }

    response = httpx.post(
        config_url,
        json=config.to_dict(),
        headers=headers,
    )

    response.raise_for_status()
    return response
