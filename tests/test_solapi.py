import unittest
from unittest.mock import Mock, patch
from typing import Dict, List, Any

from solapi.sms.sms import SMS
from solapi.sms.lms import LMS
from solapi.sms.mms import MMS
from solapi.kakao_talk.alim_talk import AlimTalkOptions, AlimTalkMessage
from solapi.senders.message_senders import MessageSender


class TestSMS(unittest.TestCase):
    def test_sms_to_dict(self) -> None:
        sms: SMS = SMS(from_number="01012345678", text="Test SMS")
        result: Dict[str, str] = sms.to_dict(to_number="01087654321")
        expected: Dict[str, str] = {
            "to": "01087654321",
            "from": "01012345678",
            "text": "Test SMS",
            "type": "SMS"
        }
        self.assertEqual(result, expected)


class TestLMS(unittest.TestCase):
    def test_lms_to_dict(self) -> None:
        lms: LMS = LMS(from_number="01012345678", text="Test LMS", subject="Test Subject")
        result: Dict[str, str] = lms.to_dict(to_number="01087654321")
        expected: Dict[str, str] = {
            "to": "01087654321",
            "from": "01012345678",
            "text": "Test LMS",
            "subject": "Test Subject",
            "type": "LMS"
        }
        self.assertEqual(result, expected)


class TestMMS(unittest.TestCase):
    def test_mms_to_dict(self) -> None:
        mms: MMS = MMS(from_number="01012345678", text="Test MMS", subject="Test Subject", file_id="FILE_ID_123")
        result: Dict[str, str] = mms.to_dict(to_number="01087654321")
        expected: Dict[str, str] = {
            "to": "01087654321",
            "from": "01012345678",
            "text": "Test MMS",
            "subject": "Test Subject",
            "type": "MMS",
            "fileId": "FILE_ID_123"
        }
        self.assertEqual(result, expected)


class TestAlimTalk(unittest.TestCase):
    def test_alimtalk_options_to_dict(self) -> None:
        options: AlimTalkOptions = AlimTalkOptions(
            pf_id="TEST_PF_ID",
            template_id="TEST_TEMPLATE_ID",
            disable_sms=True,
            variables={"#{변수1}": "값1", "#{변수2}": "값2"}
        )
        result: Dict[str, Any] = options.to_dict()
        expected: Dict[str, Any] = {
            "pfId": "TEST_PF_ID",
            "templateId": "TEST_TEMPLATE_ID",
            "disableSms": True,
            "variables": {"#{변수1}": "값1", "#{변수2}": "값2"}
        }
        self.assertEqual(result, expected)

    def test_alimtalk_message_to_dict(self) -> None:
        options: AlimTalkOptions = AlimTalkOptions(
            pf_id="TEST_PF_ID",
            template_id="TEST_TEMPLATE_ID",
            disable_sms=True,
            variables={"#{변수1}": "값1", "#{변수2}": "값2"}
        )
        message: AlimTalkMessage = AlimTalkMessage(from_number="01012345678", alimtalk_options=options)
        result: Dict[str, Any] = message.to_dict(to_number="01087654321")
        expected: Dict[str, Any] = {
            "to": "01087654321",
            "from": "01012345678",
            "type": "ATA",
            "kakaoOptions": {
                "pfId": "TEST_PF_ID",
                "templateId": "TEST_TEMPLATE_ID",
                "disableSms": True,
                "variables": {"#{변수1}": "값1", "#{변수2}": "값2"}
            }
        }
        self.assertEqual(result, expected)


class TestMessageSender(unittest.TestCase):
    def setUp(self) -> None:
        self.config: Mock = Mock()
        self.config.api_key = "test_api_key"
        self.config.secret_key = "test_secret_key"
        self.config.get_url = Mock(return_value="https://api.solapi.com")
        self.sender: MessageSender = MessageSender(self.config)

    @patch('solapi.request.requests.post')
    def test_send_one(self, mock_post: Mock) -> None:
        mock_response: Mock = Mock()
        mock_response.json.return_value = {"messageId": "TEST_MESSAGE_ID"}
        mock_post.return_value = mock_response

        message: SMS = SMS(from_number="01012345678", text="Test SMS")
        result: Dict[str, str] = self.sender.send_one(message, "01087654321")

        mock_post.assert_called_once()
        self.assertEqual(result, {"messageId": "TEST_MESSAGE_ID"})

    @patch('solapi.request.requests.post')
    def test_send_many(self, mock_post: Mock) -> None:
        mock_response: Mock = Mock()
        mock_response.json.return_value = {"messageIds": ["ID1", "ID2"]}
        mock_post.return_value = mock_response

        message: SMS = SMS(from_number="01012345678", text="Test SMS")
        result: Dict[str, List[str]] = self.sender.send_many(message, ["01087654321", "01098765432"])

        mock_post.assert_called_once()
        self.assertEqual(result, {"messageIds": ["ID1", "ID2"]})

    def test_create_message_sms(self) -> None:
        request: Mock = Mock()
        request.data = {
            "from_number": "01012345678",
            "text": "Test SMS"
        }
        message: SMS = self.sender.create_message(request)
        self.assertIsInstance(message, SMS)

    def test_create_message_lms(self) -> None:
        request: Mock = Mock()
        request.data = {
            "from_number": "01012345678",
            "text": "Test LMS" * 10,  # Make sure it's longer than 45 characters
            "subject": "Test Subject"
        }
        message: LMS = self.sender.create_message(request)
        self.assertIsInstance(message, LMS)

    def test_create_message_mms(self) -> None:
        request: Mock = Mock()
        request.data = {
            "from_number": "01012345678",
            "text": "Test MMS",
            "subject": "Test Subject",
            "image_id": "IMAGE_ID_123"
        }
        message: MMS = self.sender.create_message(request)
        self.assertIsInstance(message, MMS)

    def test_create_message_alimtalk(self) -> None:
        request: Mock = Mock()
        request.data = {
            "from_number": "01012345678",
            "pf_id": "TEST_PF_ID",
            "template_id": "TEST_TEMPLATE_ID",
            "variables": {"#{변수1}": "값1", "#{변수2}": "값2"}
        }
        message: AlimTalkMessage = self.sender.create_message(request)
        self.assertIsInstance(message, AlimTalkMessage)
        self.assertEqual(message.from_number, "01012345678")
        self.assertEqual(message.alimtalk_options.pf_id, "TEST_PF_ID")
        self.assertEqual(message.alimtalk_options.template_id, "TEST_TEMPLATE_ID")
        self.assertEqual(message.alimtalk_options.variables, {"#{변수1}": "값1", "#{변수2}": "값2"})


if __name__ == '__main__':
    unittest.main()