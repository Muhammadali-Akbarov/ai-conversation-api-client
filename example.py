"""
This module provides an example of how to use the ConversationAPI client.

It demonstrates how to initialize the API client, send a prompt, and handle
both full and chunked responses from the specified API endpoint.
"""
from typing import Generator

from conversation.client import ConversationAPI

api = ConversationAPI()
PROMPT = "Gimme ten programming languages name."

result = api.enter_prompt(prompt=PROMPT, chunked=False)

if isinstance(result, Generator):
    for chunk in result:
        print(chunk, end='', flush=True)

else:
    print(result)
