from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    def dsn(self) -> str:
        return f"postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
