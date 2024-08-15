from typing import Dict, List


from solapi.kakao_talk.alim_talk import AlimTalkOptions, AlimTalkMessage
from solapi.message import Message
from solapi.request import post, default_agent
from solapi.sms.lms import LMS
from solapi.sms.mms import MMS
from solapi.sms.sms import SMS


class MessageSender:
    def __init__(self, config):
        self.config = config

    def send_one(self, message: Message) -> Dict:
        data = {
            "message": message.to_dict(),
            "agent": self.get_agent()
        }
        return post(self.config, '/messages/v4/send', data)

    def send_many(self, messages: List[Message]) -> Dict:
        data = {
            "messages": [message.to_dict() for message in messages],
            "agent": self.get_agent()
        }
        return post(self.config, '/messages/v4/send-many', data)

    @staticmethod
    def get_agent():
        return default_agent

    def create_message(self, validated_data: Dict) -> Message:
        from_number = validated_data['from_number']
        to_number = validated_data['to_number']
        scheduled_date = validated_data.get('scheduled_date')

        if 'pf_id' in validated_data and 'template_id' in validated_data:
            return AlimTalkMessage(
                from_number,
                to_number,
                validated_data['pf_id'],
                validated_data['template_id'],
                validated_data.get('variables', {}),
                validated_data.get('disable_sms', False),
                scheduled_date
            )
        elif 'image_id' in validated_data:
            return MMS(
                from_number,
                to_number,
                validated_data['text'],
                validated_data['subject'],
                validated_data['image_id'],
                scheduled_date
            )
        elif 'subject' in validated_data or len(validated_data.get('text', '')) > 45:
            return LMS(
                from_number,
                to_number,
                validated_data['text'],
                validated_data.get('subject', ''),
                scheduled_date
            )
        else:
            return SMS(from_number, to_number, validated_data['text'], scheduled_date)