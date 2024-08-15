# SolApi Messages Python Library

SolApi Messages는 SolApi 서비스를 사용하여 문자메시지와 카카오 알림톡을 쉽게 전송할 수 있게 해주는 Python 라이브러리입니다. 

## 주요 기능

- SMS, LMS, MMS 메시지 전송
- 단일 및 대량 메시지 전송
- 예약 발송
- 메시지 길이에 따른 자동 유형 전환
- 이미지 파일이 존재할 경우 MMS로 자동 전환
- 카카오 알림톡 전송

## 설치

pip를 사용하여 라이브러리를 설치할 수 있습니다.

```bash
pip install python-solapi-messages
```

## 사용법

### 환경설정
SolAPI에서 발급받은 키를 사용해 설정을 초기화해주세요.

```python
from solapi.config import SolApiConfig

config = SolApiConfig(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")

```
### SMS 전송
```python
from solapi.sms.sms import SMS
from solapi.senders.message_senders import MessageSender

sender = MessageSender(config)
message = SMS(from_number="01012345678", text="Hello, World!")
result = sender.send_one(message, to_number="01087654321")
print(result)
```
### LMS 전송
```python
from solapi.sms.lms import LMS

message = LMS(from_number="01012345678", text="긴 메시지 내용", subject="제목")
result = sender.send_one(message, to_number="01087654321")
print(result)
```
### MMS 전송
```python
from solapi.sms.mms import MMS

message = MMS(from_number="01012345678", text="MMS 메시지", subject="MMS 제목", file_id="FILE_ID")
result = sender.send_one(message, to_number="01087654321")
print(result)
```
### 알림톡 전송
```python
from solapi.kakao_talk.alim_talk import AlimTalkOptions, AlimTalkMessage

options = AlimTalkOptions(pf_id="PFID", template_id="TEMPLATE_ID", variables={"VAR1": "값1"})
message = AlimTalkMessage(from_number="01012345678", alimtalk_options=options)
result = sender.send_one(message, to_number="01087654321")
print(result)
```
### 대량 발송
send_many 메소드를 사용하면 여러 수신자에게 동일한 메시지를 보낼 수 있습니다.
```python
to_numbers = ["01087654321", "01098765432", "01076543210"]
result = sender.send_many(message, to_numbers)
print(result)
```
### 예약 발송
scheduled_date 파라미터를 사용하면 원하는 발송 시간을 정할 수 있습니다.
```python
import datetime

scheduled_time = datetime.datetime.now() + datetime.timedelta(hours=1)  # 1시간 후 발송
message = SMS(from_number="01012345678", text="예약된 메시지입니다.", scheduled_date=scheduled_time)
result = sender.send_one(message, to_number="01087654321")
print(result)
```
### 이미지 업로드
이미지를 먼저 업로드해야 fileId를 얻을 수 있습니다.
```python
import datetime

from solapi.storage import upload_image

response = upload_image("path/to/image.jpg", config)
file_id = response.json()['fileId']
```
## 테스트
아래 코드를 입력하시면 테스트를 실행할 수 있습니다.
```bash
python -m unittest discover tests
```
## 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.