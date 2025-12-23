from enum import Enum


class MessageStatusConstants(str, Enum):
    """ Constants for the status of message """

    SUCCESS = "Success"
    FAILED = "Failed"
    PENDING = "Pending"
