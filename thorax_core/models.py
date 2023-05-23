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

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        mrf_simple = [
            config for config in data if "db" in config and config["db"][0] == ":accept"
        ][0]

        instances = [
            tup for tup in mrf_simple["value"] if tup["tuple"][0] == ":accept"
        ][0]["tuple"][1]
        return Config(
            allowlist=[Instance.from_dict(instance) for instance in instances]
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
                        }
                    ],
                }
            ]
        }
