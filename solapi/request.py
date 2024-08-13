import requests
from .auth import get_headers


def _make_request(config, method, path, data=None, headers=None):
    url = config.get_url(path)
    headers = headers or {}
    headers.update(get_headers(config.api_key, config.secret_key))

    if method == 'GET':
        return requests.get(url, headers=headers)
    elif method == 'POST':
        return requests.post(url, headers=headers, json=data)
    elif method == 'PUT':
        return requests.put(url, headers=headers, json=data)
    elif method == 'DELETE':
        if data:
            return requests.delete(url, headers=headers, json=data)
        else:
            return requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")


def post(config, path, data):
    return _make_request(config, 'POST', path, data=data)


def get(config, path):
    return _make_request(config, 'GET', path)


def put(config, path, data):
    return _make_request(config, 'PUT', path, data=data)


def delete(config, path, data=None):
    return _make_request(config, 'DELETE', path, data=data)