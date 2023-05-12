import httpx
import json
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


config_url = f"https://{config['host']}/api/v1/pleroma/admin/config"
headers = {"Authorization": f"Bearer {config['token']}"}


def get_configs(from_api=True) -> dict:
    if from_api:
        response = httpx.get(config_url, headers=headers)
        assert response.status_code == 200, f"{response.status_code}: {response.json()}"
        configs = response.json()["configs"]
    else:
        configs = json.loads(open("./out.json", "r").read())["configs"]
    return configs


def get_instances() -> list[str]:
    configs = get_configs(from_api=True)

    mrf_simple = [
        config for config in configs if "db" in config and config["db"][0] == ":accept"
    ][0]

    instances = [tup for tup in mrf_simple["value"] if tup["tuple"][0] == ":accept"][0][
        "tuple"
    ][1]

    # Optional formatting for wiki table format
    # wikitable = '{| class="wikitable"\n|+!' + '\n|-\n|'.join(instances) + '\n|}'
    # print(wikitable)
    return instances


def add_instance(instance: str) -> None:
    instances = get_instances()
    instances.append(
        {
            "tuple": [
                instance,
                "",
            ]
        }
    )

    post_data = {
        "configs": [
            {
                "group": ":pleroma",
                "key": ":mrf_simple",
                "value": [
                    {
                        "tuple": [
                            ":accept",
                            instances,
                        ]
                    }
                ],
            }
        ]
    }
    bonus_headers = {
        "Content-Type": "application/json;charset=utf-8",
    }

    response = httpx.post(
        config_url,
        data=json.dumps(post_data),
        headers=headers | bonus_headers,
    )


def list_instances() -> list[str]:
    instances = get_instances()
    instances = [instance["tuple"][0] for instance in instances]

    instances.sort()
    return instances


if __name__ == "__main__":
    add_instance("test3")
