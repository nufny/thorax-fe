from app.api import get_config, update_configs
from app.models import Instance


def add_instance(instance_url: str, reason: str = "") -> None:
    config = get_config()
    if instance_url in [instance.url for instance in config.allowlist]:
        raise ValueError(f"Attempting to add already added instance: {instance_url}")
    config.allowlist.append(Instance(url=instance_url, reason=reason))

    update_configs(config)
    print(f"Successfully added {instance_url}")


def remove_instance(instance_url: str) -> None:
    config = get_config()
    allowlist_urls = [instance.url for instance in config.allowlist]
    if instance_url not in allowlist_urls:
        raise ValueError(f'Instance: "{instance_url}" not in allowlist!')

    i = allowlist_urls.index(instance_url)
    del config.allowlist[i]

    update_configs(config)
    print(f"Successfully removed {instance_url}")


def list_instances() -> list[str]:
    config = get_config()
    allowlist_urls = [instance.url for instance in config.allowlist]
    allowlist_urls.sort()
    return allowlist_urls
