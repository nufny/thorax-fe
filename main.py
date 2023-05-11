import httpx
import json


config_url = "https://ak.zweitekassabitte.jetzt/api/v1/pleroma/admin/config"
headers = {"Authorization": "Bearer [REDACTED FOR GIT]"}


def get_configs(from_api=True) -> dict:
    if from_api:
        response = httpx.get(config_url, headers=headers)

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
    """
    Currently doesn't work
    """
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
                "db": [":accept"],
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
        "Content-Types": "application/json;charset=utf-8",
    }
    post_data = json.loads(open("in.json").read())
    response = httpx.post(
        config_url,
        data=post_data,
        headers=headers | bonus_headers,
    )
    breakpoint()
    print(response)


def list_instances() -> list[str]:
    instances = get_instances()
    instances = [instance["tuple"][0] for instance in instances]

    instances.sort()
    return instances


if __name__ == "__main__":
    print(list_instances())
