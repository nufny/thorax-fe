import json
import tomllib

import httpx

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


def get_instances() -> list[dict[str, list[str]]]:
    configs = get_configs(from_api=True)

    mrf_simple = [
        config for config in configs if "db" in config and config["db"][0] == ":accept"
    ][0]

    instances = [tup for tup in mrf_simple["value"] if tup["tuple"][0] == ":accept"][0][
        "tuple"
    ][1]

    # TODO: remove this later
    # Optional formatting for wiki table format
    # wikitable = '{| class="wikitable"\n|+!' + '\n|-\n|'.join(instances) + '\n|}'
    # print(wikitable)
    return instances


def construct_set_request() -> dict:
    instances = get_instances()

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
    return post_data


def _get_instance_list_from_post_data(post_data: dict) -> list:
    return post_data["configs"][0]["value"][0]["tuple"][1]


def update_allowlist(post_data: dict) -> None:
    bonus_headers = {
        "Content-Type": "application/json;charset=utf-8",
    }

    response = httpx.post(
        config_url,
        json=post_data,
        headers=headers | bonus_headers,
    )

    response.raise_for_status()


def add_instance(instance: str) -> None:
    post_data = construct_set_request()
    instance_list = _get_instance_list_from_post_data(post_data)
    if instance in [inst["tuple"][0] for inst in instance_list]:
        raise ValueError(f"Attempting to add already added instance: {instance}")
    instance_list.append(
        {
            "tuple": [
                instance,
                "",
            ]
        }
    )

    update_allowlist(post_data)
    print(f"Successfully added {instance}")


def remove_instance(instance: str) -> None:
    post_data = construct_set_request()
    instance_list = _get_instance_list_from_post_data(post_data)

    instance_names: list = [entry["tuple"][0] for entry in instance_list]
    if instance not in instance_names:
        raise ValueError(f'Instance: "{instance}" not in allowlist!')

    for i in range(len(instance_list)):
        if instance_list[i]["tuple"][0] == instance:
            del instance_list[i]
            break

    update_allowlist(post_data)
    print(f"Successfully removed {instance}")


def list_instances() -> list[str]:
    instances = get_instances()
    simple_instances = [instance["tuple"][0] for instance in instances]

    simple_instances.sort()
    return simple_instances


if __name__ == "__main__":
    test_instance = "test1.example.org"
    add_instance(test_instance)
    assert test_instance in list_instances()
    remove_instance(test_instance)
    assert test_instance not in list_instances()
