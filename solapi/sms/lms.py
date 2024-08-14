from typing import Dict

from solapi.message import Message


class LMS(Message):
    def __init__(self, from_number: str, text: str, subject: str = None, scheduled_date: str = None):
        super().__init__(from_number, text, scheduled_date)
        self.subject = subject

    def to_dict(self, to_number: str) -> Dict:
        message_dict = {
            "to": to_number,
            "from": self.from_number,
            "text": self.text,
            "type": "LMS"
        }
        if self.subject:
            message_dict["subject"] = self.subject
        if self.scheduled_date:
            message_dict["scheduledDate"] = self.scheduled_date.isoformat()
        return message_dict
