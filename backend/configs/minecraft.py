from dataclasses import dataclass

from configs.settings import settings


# Настройки подключения к Minecraft-серверу: адрес, порт и параметры RCON
@dataclass(slots=True)
class MinecraftConfig:
    host: str | None = settings.MINECRAFT_HOST
    port: int | None = settings.MINECRAFT_PORT
    rcon_port: int | None = settings.MINECRAFT_RCON_PORT
    rcon_password: str | None = settings.MINECRAFT_RCON_PASSWORD


mc_config = MinecraftConfig()
