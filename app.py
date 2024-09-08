"""
This module provides an interface for interacting with a conversation API.

It includes a ConversationAPI class that allows users to send prompts and
receive responses from a specified API endpoint.
"""
import json
from abc import ABC, abstractmethod

import requests


class APIClient(ABC):
    """
    Abstract base class for API clients.
    """

    @abstractmethod
    def send_request(self, data):
        """
        Send a request to the API.
        """


class ConversationAPIClient(APIClient):
    """Client for interacting with the conversation API."""

    def __init__(self, base_url='http://127.0.0.1:8080'):
        """
        Initialize the ConversationAPIClient.

        Args:
            base_url (str): The base URL of the API.
        """
        self.base_url = base_url

    def send_request(self, data, timeout=30):
        """
        Send a request to the API.

        Args:
            data (dict): The data to send in the request.
            timeout (int): The timeout for the request in seconds.

        Returns:
            requests.Response: The response from the API.
        """
        url = f"{self.base_url}/backend-api/v2/conversation"
        return requests.post(url, json=data, stream=True, timeout=timeout)


class ResponseParser:
    """Parser for API responses."""

    @staticmethod
    def parse_response(response):
        """
        Parse the response from the API.

        Args:
            response (requests.Response): The response to parse.

        Returns:
            str: The parsed response content.
        """
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('{"type": "content", "content":'):
                    content = json.loads(decoded_line)['content']
                    full_response += content
        return full_response


class ConversationAPI:
    """Main class for interacting with the conversation API."""

    def __init__(self, client=None, parser=None):
        """
        Initialize the ConversationAPI.

        Args:
            client (APIClient): The API client to use.
            parser (ResponseParser): The response parser to use.
        """
        self.client = client or ConversationAPIClient()
        self.parser = parser or ResponseParser()

    def enter_prompt(
        self, prompt, model="", web_search=False,
        provider="", auto_continue=True, api_key=None
    ):
        """
        Send a prompt to the API and get the response.

        Args:
            prompt (str): The prompt to send.
            model (str): The model to use.
            web_search (bool): Whether to use web search.
            provider (str): The provider to use.
            auto_continue (bool): Whether to auto-continue.
            api_key (str): The API key to use.

        Returns:
            str: The response from the API.
        """
        data = {
          "model": model,
          "web_search": web_search,
          "provider": provider,
          "messages": [{"role": "user", "content": prompt}],
          "auto_continue": auto_continue,
          "api_key": api_key
        }

        response = self.client.send_request(data)
        full_response = self.parser.parse_response(response)

        try:
            response.close()  # Ensure the response is closed properly
        except requests.exceptions.StreamConsumedError:
            pass
        except requests.RequestException:
            pass

        return full_response


api = ConversationAPI()


def ask_question():
    """
    Continuously ask for prompts and get responses from the API.
    """
    while True:
        prompt = input("Enter your prompt (or 'quit' to exit): ")
        if prompt.lower() == 'quit':
            break
        result = api.enter_prompt(prompt)
        print(result)


if __name__ == "__main__":
    ask_question()
