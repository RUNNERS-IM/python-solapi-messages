import unittest
from datetime import datetime
from solapi.sms.message import SMS, LMS, MMS


class TestMessageTypes(unittest.TestCase):
    def test_sms_creation(self):
        sms = SMS("029302266", "Test SMS")
        self.assertEqual(sms.from_number, "029302266")
        self.assertEqual(sms.text, "Test SMS")
        self.assertIsNone(sms.scheduled_date)

    def test_sms_to_dict(self):
        sms = SMS("029302266", "Test SMS")
        result = sms.to_dict("01012345678")
        expected = {
            "to": "01012345678",
            "from": "029302266",
            "text": "Test SMS",
            "type": "SMS"
        }
        self.assertEqual(result, expected)

    def test_sms_with_scheduled_date(self):
        scheduled_date = datetime(2023, 12, 31, 23, 59, 59)
        sms = SMS("029302266", "Scheduled SMS", scheduled_date=scheduled_date)
        result = sms.to_dict("01012345678")
        self.assertEqual(result["scheduledDate"], scheduled_date.isoformat())

    def test_lms_creation(self):
        lms = LMS("029302266", "Test LMS Content", "Test Subject")
        self.assertEqual(lms.from_number, "029302266")
        self.assertEqual(lms.text, "Test LMS Content")
        self.assertEqual(lms.subject, "Test Subject")
        self.assertIsNone(lms.scheduled_date)

    def test_lms_to_dict(self):
        lms = LMS("029302266", "Test LMS Content", "Test Subject")
        result = lms.to_dict("01012345678")
        expected = {
            "to": "01012345678",
            "from": "029302266",
            "text": "Test LMS Content",
            "subject": "Test Subject",
            "type": "LMS"
        }
        self.assertEqual(result, expected)

    def test_lms_with_scheduled_date(self):
        scheduled_date = datetime(2023, 12, 31, 23, 59, 59)
        lms = LMS("029302266", "Scheduled LMS Content", "Test Subject", scheduled_date=scheduled_date)
        result = lms.to_dict("01012345678")
        self.assertEqual(result["scheduledDate"], scheduled_date.isoformat())

    def test_mms_creation(self):
        mms = MMS("029302266", "Test MMS Content", "Test Subject", "test_file_id")
        self.assertEqual(mms.from_number, "029302266")
        self.assertEqual(mms.text, "Test MMS Content")
        self.assertEqual(mms.subject, "Test Subject")
        self.assertEqual(mms.file_id, "test_file_id")
        self.assertIsNone(mms.scheduled_date)

    def test_mms_to_dict(self):
        mms = MMS("029302266", "Test MMS Content", "Test Subject", "test_file_id")
        result = mms.to_dict("01012345678")
        expected = {
            "to": "01012345678",
            "from": "029302266",
            "text": "Test MMS Content",
            "subject": "Test Subject",
            "type": "MMS",
            "fileId": "test_file_id"
        }
        self.assertEqual(result, expected)

    def test_mms_with_scheduled_date(self):
        scheduled_date = datetime(2023, 12, 31, 23, 59, 59)
        mms = MMS("029302266", "Scheduled MMS", "Test Subject", "test_file_id", scheduled_date=scheduled_date)
        result = mms.to_dict("01012345678")
        self.assertEqual(result["scheduledDate"], scheduled_date.isoformat())


if __name__ == '__main__':
    unittest.main()
