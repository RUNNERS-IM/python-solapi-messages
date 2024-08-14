from typing import Dict

from solapi.sms.lms import LMS


class MMS(LMS):
    def __init__(self, from_number: str, text: str, subject: str = None, file_id: str = None,
                 scheduled_date: str = None):
        super().__init__(from_number, text, subject, scheduled_date)
        self.file_id = file_id

    def to_dict(self, to_number: str) -> Dict:
        message_dict = super().to_dict(to_number)
        message_dict.update({
            "type": "MMS",
            "fileId": self.file_id
        })
        return message_dict
