from abc import ABC, abstractmethod
from typing import Dict, Optional


class Message(ABC):
    def __init__(self, from_number: str, to_number: str, scheduled_date: Optional[str] = None):
        self.from_number = from_number
        self.to_number = to_number
        self.scheduled_date = scheduled_date

    @abstractmethod
    def to_dict(self) -> Dict:
        base_dict = {
            "to": self.to_number,
            "from": self.from_number
        }
        if self.scheduled_date:
            base_dict["scheduledDate"] = self.scheduled_date
        return base_dict
