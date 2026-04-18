import secrets

from mcdreforged.api.utils.serializer import Serializable


class Config(Serializable):
    token: str = secrets.token_hex(16)
