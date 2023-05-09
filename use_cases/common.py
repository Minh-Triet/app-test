"""Contains some general purpose functions that are used across several use cases.
"""
from development_config import Config
import random
import string

from google.protobuf.message import Message


def generate_name(brokerage_id: str, max_length):
    """Returns random string with following pattern and given maximum length
    {brokerage_id}_{random combination of numbers and letters}.
    {brokerage_id} prefix is used, so entities that created with samples can be easily enough distinguished.
    """
    return f"{brokerage_id}_" + \
           ''.join(
               random.choice(string.ascii_letters + string.digits) for _ in range(max_length - len(brokerage_id) - 1))


def fill_contact_information(contact_information: Message, config: Config):
    """Fills given object with some random data for demonstration purpose.
    This is acceptable for Stage environment, but make sure using correct data in Production.
    """
    email = contact_information.email.add()
    email.email = config.email
    contact_information.first_name = generate_name(config.brokerage_id, 20)
    contact_information.last_name = generate_name(config.brokerage_id, 25)

    return contact_information
