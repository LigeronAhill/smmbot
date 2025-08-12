import tomllib

from config.vk import VkConfig

from .database import DBConfig


class Config:
    bot_token: str
    db_config: DBConfig
    vk: VkConfig

    def __init__(self, filename: str):
        with open(filename, "rb") as f:
            parsed = tomllib.load(f)
            self.bot_token = parsed["bot"]["token"]
            host = parsed["postgres"]["host"]
            port = parsed["postgres"]["port"]
            user = parsed["postgres"]["user"]
            password = parsed["postgres"]["password"]
            database = parsed["postgres"]["database"]
            self.db_config = DBConfig(host, port, user, password, database)
            access_token = parsed["vk"]["access_token"]
            group_domain = parsed["vk"]["group_domain"]
            group_id = parsed["vk"]["group_id"]
            self.vk = VkConfig(access_token, group_domain, group_id)
