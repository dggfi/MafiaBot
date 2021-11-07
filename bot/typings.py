from typing import TypedDict, Literal

class IConfig(TypedDict):
    token: str
    description: str
    default_command_prefix: str
    owner_id: str
    bot_public: bool
    suppress_configuration_warnings: bool
    host: str
    port: int