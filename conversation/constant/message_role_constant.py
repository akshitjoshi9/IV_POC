from enum import Enum


class MessageRoleConstants(str, Enum):
    """ Constants for the role of message """

    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"
