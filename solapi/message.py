
class Message:
    def __init__(self, from_number: str, text: str, scheduled_date=None):
        self.from_number = from_number
        self.text = text
        self.scheduled_date = scheduled_date

    def to_dict(self, to_number: str) -> dict:
        message_dict = {
            "to": to_number,
            "from": self.from_number,
            "text": self.text
        }
        if self.scheduled_date:
            message_dict["scheduledDate"] = self.scheduled_date
        return message_dict