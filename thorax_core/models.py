import pydantic


class Instance(pydantic.BaseModel):
    url: str
    reason: str

    @classmethod
    def from_dict(cls, data: dict[str, list[str]]):
        url, reason = data["tuple"]
        return Instance(url=url, reason=reason)

    def to_dict(self):
        return {
            "tuple": [
                self.url,
                self.reason,
            ]
        }


class Config(pydantic.BaseModel):
    allowlist: list[Instance]
    denylist: list[Instance]

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        def parse_simple_policy(policy: str) -> list[dict]:
            config = [
                config for config in data if "db" in config and policy in config["db"]
            ]
            if len(config) == 0:
                return []
            config = config[0]
            return [tup for tup in config["value"] if tup["tuple"][0] == policy][0][
                "tuple"
            ][1]

        allowlist = parse_simple_policy(":accept")
        denylist = parse_simple_policy(":reject")

        return Config(
            allowlist=[Instance.from_dict(instance) for instance in allowlist],
            denylist=[Instance.from_dict(instance) for instance in denylist],
        )

    def to_dict(self) -> dict:
        return {
            "configs": [
                {
                    "group": ":pleroma",
                    "key": ":mrf_simple",
                    "value": [
                        {
                            "tuple": [
                                ":accept",
                                [instance.to_dict() for instance in self.allowlist],
                            ]
                        },
                        {
                            "tuple": [
                                ":reject",
                                [instance.to_dict() for instance in self.denylist],
                            ]
                        },
                    ],
                }
            ]
        }
