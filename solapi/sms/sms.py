from typing import Dict

from solapi.message import Message
from solapi.sms.base import TextMessage


class SMS(TextMessage):
    def to_dict(self) -> Dict:
        message_dict = super().to_dict()
        message_dict["type"] = "SMS"
        return message_dict