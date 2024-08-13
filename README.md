# SolApi SMS Python Library

This library provides a simple interface to send SMS messages using the SolApi service.

## Installation

You can install the library using pip:

```
pip install solapi-sms
```

## Usage

Here's a quick example of how to use the library:

```python
from solapi.sms.message import SMS, MessageSender

# Create an SMS message
sms = SMS("029302266", "Hello, World!")

# Send the message
response = MessageSender.send_one(sms, "01012345678")

print(response.json())
```

For more detailed usage instructions, please refer to the documentation.

## Running Tests
To run the tests, use the following command from the project root:

```
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.