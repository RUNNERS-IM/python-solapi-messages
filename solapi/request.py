from typing import Dict, Any, Optional

import requests

from .auth import get_headers
from .config import SolApiConfig


def _make_request(config: SolApiConfig, method: str, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    url = config.get_url(path)
    headers = headers or {}
    headers.update(get_headers(config.api_key, config.secret_key))

    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, json=data)
    elif method == 'DELETE':
        if data:
            response = requests.delete(url, headers=headers, json=data)
        else:
            response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    response.raise_for_status()
    return response.json()


def post(config: SolApiConfig, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return _make_request(config, 'POST', path, data=data)


def get(config: SolApiConfig, path: str) -> Dict[str, Any]:
    return _make_request(config, 'GET', path)


def put(config: SolApiConfig, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return _make_request(config, 'PUT', path, data=data)


def delete(config: SolApiConfig, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return _make_request(config, 'DELETE', path, data=data)