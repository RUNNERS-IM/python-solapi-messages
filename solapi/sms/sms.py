from typing import Dict

from solapi.message import Message


class SMS(Message):
    def to_dict(self, to_number: str) -> Dict:
        message_dict = {
            "to": to_number,
            "from": self.from_number,
            "text": self.text,
            "type": "SMS"
        }
        if self.scheduled_date:
            message_dict["scheduledDate"] = self.scheduled_date.isoformat()
        return message_dict
