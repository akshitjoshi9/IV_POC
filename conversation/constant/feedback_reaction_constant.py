from enum import Enum


class FeedbackReactionsConstants(str, Enum):
    """ Constants for the feedback reaction """

    NEUTRAL = "neutral"
    POSITIVE = "positive"
    NEGATIVE = "negative"
