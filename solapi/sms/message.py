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
    def __init__(self, from_number, text, subject=None, scheduled_date=None):
        super().__init__(from_number, text, scheduled_date)
        self.subject = subject

    def to_dict(self, to_number):
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


class MMS(LMS):
    def __init__(self, from_number, text, subject=None, file_id=None, scheduled_date=None):
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

    def create_message(self, request):
        """
        요청 객체에서 필요한 정보를 추출하여 적절한 메시지 객체(SMS, LMS, MMS)를 생성합니다.
        """
        from_number = request.data.get("from_number")
        text = request.data.get("text")
        subject = request.data.get("subject")
        image_id = request.data.get("image_id")
        scheduled_date = request.data.get("scheduled_date")

        # image_id가 존재하면 MMS로 전환
        if image_id:
            return MMS(from_number, text, subject=subject, file_id=image_id, scheduled_date=scheduled_date)
        # subject가 있거나 텍스트 길이가 45자를 초과하면 LMS로 전환
        elif subject or len(text) > 45:
            return LMS(from_number, text, subject=subject, scheduled_date=scheduled_date)
        # 그 외에는 SMS로 전환
        else:
            return SMS(from_number, text, scheduled_date)

