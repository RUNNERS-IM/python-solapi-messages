from typing import Optional, Dict

from solapi.message import Message


class TextMessage(Message):
    def __init__(self, from_number: str, to_number: str, text: str, scheduled_date: Optional[str] = None):
        super().__init__(from_number, to_number, scheduled_date)
        self.text = text

    def to_dict(self) -> Dict:
        message_dict = super().to_dict()
        message_dict["text"] = self.text
        return message_dict