from typing import Dict
import datetime
import hashlib
import hmac
import time
import uuid



def unique_id() -> str:
    return str(uuid.uuid1().hex)


def get_iso_datetime() -> str:
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()


def get_signature(key: str = "", msg: str = "") -> str:
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()


def get_headers(api_key: str = "", api_secret_key: str = "") -> Dict[str, str]:
    date = get_iso_datetime()
    salt = unique_id()
    data = date + salt
    headers = {
        "Authorization": "HMAC-SHA256 ApiKey="
        + api_key
        + ", Date="
        + date
        + ", salt="
        + salt
        + ", signature="
        + get_signature(api_secret_key, data),
        "Content-Type": "application/json; charset=utf-8",
    }
    return headers
