from typing import Dict, Optional

from solapi.message import Message


class AlimTalkOptions:
    def __init__(self, pf_id: str, template_id: str, disable_sms: bool = False, variables: Optional[Dict[str, str]] = None):
        self.pf_id = pf_id
        self.template_id = template_id
        self.disable_sms = disable_sms
        self.variables = variables or {}

    def to_dict(self) -> Dict:
        return {
            'pfId': self.pf_id,
            'templateId': self.template_id,
            'disableSms': self.disable_sms,
            'variables': self.variables
        }


class AlimTalkMessage(Message):
    def __init__(self, from_number: str, text: str, alimtalk_options: AlimTalkOptions, scheduled_date: Optional[str] = None):
        super().__init__(from_number, text, scheduled_date)
        self.alimtalk_options = alimtalk_options

    def to_dict(self, to_number: str) -> Dict:
        message_dict = super().to_dict(to_number)
        message_dict['type'] = 'ATA'
        message_dict['kakaoOptions'] = self.alimtalk_options.to_dict()
        return message_dict
