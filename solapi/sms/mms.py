from typing import Dict

from solapi.sms.lms import LMS


class MMS(LMS):
    def __init__(self, from_number: str, to_number: str, text: str, subject: str, image_id: str, scheduled_date: Optional[str] = None):
        super().__init__(from_number, to_number, text, subject, scheduled_date)
        self.image_id = image_id

    def to_dict(self) -> Dict:
        message_dict = super().to_dict()
        message_dict["type"] = "MMS"
        message_dict["imageId"] = self.image_id
        return message_dict