from typing import Dict, Any, Optional

import requests
import json

from solapi.auth import get_headers
from solapi.config import SolApiConfig


def add_kakao_template(config: SolApiConfig, template_data: Dict[str, Any]) -> Optional[Any]:
    url = config.get_url("/kakao/v2/templates")
    headers = get_headers(config.api_key, config.secret_key)

    try:
        response = requests.post(url, headers=headers, json=template_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


def create_template_data(
        name: str,
        content: str,
        category_code: str,
        message_type: str = "BA",
        emphasize_type: str = "NONE",
        buttons: list = None,
        extra: str = None,
        ad: str = None
) -> Dict[str, Any]:
    template_data = {
        "name": name,
        "content": content,
        "categoryCode": category_code,
        "messageType": message_type,
        "emphasizeType": emphasize_type
    }

    if buttons:
        template_data["buttons"] = buttons
    if extra:
        template_data["extra"] = extra
    if ad:
        template_data["ad"] = ad

    return template_data
