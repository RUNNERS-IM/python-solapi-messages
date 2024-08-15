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

    def send_one(self, message: Message, to_number: str) -> Dict:
        data = {
            "message": message.to_dict(to_number),
            "agent": self.get_agent()
        }
        return post(self.config, '/messages/v4/send', data)

    def send_many(self, message: Message, to_numbers: List[str]) -> Dict:
        data = {
            "messages": [message.to_dict(number) for number in to_numbers],
            "agent": self.get_agent()
        }
        return post(self.config, '/messages/v4/send-many', data)

    @staticmethod
    def get_agent():
        return default_agent

    def create_message(self, request):
        from_number = request.data.get('from_number')
        text = request.data.get('text', '')
        subject = request.data.get('subject')
        image_id = request.data.get('image_id')
        scheduled_date = request.data.get('scheduled_date')

        if 'pf_id' in request.data and 'template_id' in request.data:
            alimtalk_options = AlimTalkOptions(
                pf_id=request.data['pf_id'],
                template_id=request.data['template_id'],
                disable_sms=request.data.get('disable_sms', False),
                variables=request.data.get('variables', {})
            )
            return AlimTalkMessage(from_number, alimtalk_options, scheduled_date)
        elif image_id:
            return MMS(from_number, text, subject, image_id, scheduled_date)
        elif subject or len(text) > 45:
            return LMS(from_number, text, subject, scheduled_date)
        else:
            return SMS(from_number, text, scheduled_date)