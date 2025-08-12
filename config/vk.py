class VkConfig:
    access_token: str
    group_domain: str
    group_id: int

    def __init__(
        self, access_token: str, group_domain: str, group_id: int
    ) -> None:
        self.access_token = access_token
        self.group_domain = group_domain
        self.group_id = group_id
