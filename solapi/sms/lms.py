from typing import Dict

from solapi.sms.base import TextMessage


class LMS(TextMessage):
    def __init__(self, from_number: str, to_number: str, text: str, subject: str, scheduled_date: Optional[str] = None):
        super().__init__(from_number, to_number, text, scheduled_date)
        self.subject = subject

    def to_dict(self) -> Dict:
        message_dict = super().to_dict()
        message_dict["type"] = "LMS"
        message_dict["subject"] = self.subject
        return message_dict
