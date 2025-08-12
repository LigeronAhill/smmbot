from vk_api import VkApi
from vk_api.upload import VkApiMethod

from config.vk import VkConfig


class VkClient:
    access_token: str
    group_domain: str
    group_id: int

    def __init__(self, config: VkConfig) -> None:
        self.access_token = config.access_token
        self.group_domain = config.group_domain
        self.group_id = config.group_id

    def get_api(self) -> VkApiMethod:
        vk_session = VkApi(token=self.access_token)
        return vk_session.get_api()
