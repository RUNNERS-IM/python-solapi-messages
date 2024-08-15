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
    def __init__(self, from_number: str, to_number: str, pf_id: str, template_id: str, variables: Dict[str, str], disable_sms: bool = False, scheduled_date: Optional[str] = None):
        super().__init__(from_number, to_number, scheduled_date)
        self.pf_id = pf_id
        self.template_id = template_id
        self.variables = variables
        self.disable_sms = disable_sms

    def to_dict(self) -> Dict:
        message_dict = super().to_dict()
        message_dict["type"] = "ATA"
        message_dict["kakaoOptions"] = {
            "pfId": self.pf_id,
            "templateId": self.template_id,
            "variables": self.variables,
            "disableSms": self.disable_sms
        }
        return message_dict