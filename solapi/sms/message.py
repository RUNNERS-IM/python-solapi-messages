from abc import ABC, abstractmethod
import platform
from solapi.request import post

default_agent = {
    'sdkVersion': 'python/4.2.0',
    'osPlatform': platform.platform() + " | " + platform.python_version()
}


class Message(ABC):
    def __init__(self, from_number, text, scheduled_date=None):
        self.from_number = from_number
        self.text = text
        self.scheduled_date = scheduled_date

    @abstractmethod
    def to_dict(self, to_number):
        pass


class SMS(Message):
    def to_dict(self, to_number):
        message_dict = {
            "to": to_number,
            "from": self.from_number,
            "text": self.text,
            "type": "SMS"
        }
        if self.scheduled_date:
            message_dict["scheduledDate"] = self.scheduled_date.isoformat()
        return message_dict


class LMS(Message):
    def __init__(self, from_number, text, subject, scheduled_date=None):
        super().__init__(from_number, text, scheduled_date)
        self.subject = subject

    def to_dict(self, to_number):
        message_dict = {
            "to": to_number,
            "from": self.from_number,
            "text": self.text,
            "subject": self.subject,
            "type": "LMS"
        }
        if self.scheduled_date:
            message_dict["scheduledDate"] = self.scheduled_date.isoformat()
        return message_dict


class MMS(LMS):
    def __init__(self, from_number, text, subject, file_id, scheduled_date=None):
        super().__init__(from_number, text, subject, scheduled_date)
        self.file_id = file_id

    def to_dict(self, to_number):
        message_dict = super().to_dict(to_number)
        message_dict.update({
            "type": "MMS",
            "fileId": self.file_id
        })
        return message_dict


class MessageSender:
    def __init__(self, config):
        self.config = config

    def send_one(self, message, to_number):
        data = {
            "message": message.to_dict(to_number),
            "agent": self.get_agent()
        }
        return post(self.config, '/messages/v4/send', data)

    def send_many(self, message, to_numbers):
        data = {
            "messages": [message.to_dict(number) for number in to_numbers],
            "agent": self.get_agent()
        }
        return post(self.config, '/messages/v4/send-many', data)

    @staticmethod
    def get_agent():
        return default_agent

    def create_message(self, from_number, text, image_id=None, scheduled_date=None):
        """
        문자 메시지의 길이와 이미지 ID 존재 여부에 따라 SMS, LMS 또는 MMS 객체를 반환합니다.
        """
        if image_id:
            return MMS(from_number, text, "MMS 자동 전환", file_id=image_id, scheduled_date=scheduled_date)
        elif len(text) > 45:  # 텍스트 길이가 45자를 초과하면 LMS로 전환
            return LMS(from_number, text, subject="LMS 자동 전환", scheduled_date=scheduled_date)
        else:
            return SMS(from_number, text, scheduled_date)