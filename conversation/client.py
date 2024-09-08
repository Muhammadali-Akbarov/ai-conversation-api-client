"""
This module provides an interface for interacting with a conversation API.

It includes a ConversationAPI class that allows users to send prompts and
receive responses from a specified API endpoint. It supports both full and
chunked responses.
"""
import json

from abc import ABC, abstractmethod
from typing import Generator, Union

import requests


class APIClient(ABC):
    """
    Abstract base class for API clients.
    """

    @abstractmethod
    def send_request(self, data: dict) -> requests.Response:
        """
        Send a request to the API.
        """


class ConversationAPIClient(APIClient):
    """
    Client for interacting with the conversation API.
    """
    def __init__(self, base_url: str = 'http://127.0.0.1:8080'):
        """
        Initialize the ConversationAPIClient.

        Args:
            base_url (str): The base URL of the API.
        """
        self.base_url = base_url

    def send_request(self, data: dict, timeout: int = 30) -> requests.Response:
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
    def parse_response(
        response: requests.Response,
        chunked: bool = False  # Renamed parameter
    ) -> Union[str, Generator[str, None, None]]:
        """
        Parse the response from the API.

        Args:
            response (requests.Response): The response to parse.
            chunked (bool): Whether to return chunks or full response.

        Returns:
            Union[str, Generator[str, None, None]]: The parsed response
            content.
        """
        def parse_chunks():
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith(
                        '{"type": "content", "content":'
                    ):
                        content = json.loads(decoded_line)['content']
                        yield content

        if chunked:  # Updated usage
            return parse_chunks()
        else:
            return "".join(parse_chunks())


class ConversationAPI:
    """Main class for interacting with the conversation API."""

    def __init__(
        self,
        client: APIClient = None,
        parser: ResponseParser = None
    ):
        """
        Initialize the ConversationAPI.

        Args:
            client (APIClient): The API client to use.
            parser (ResponseParser): The response parser to use.
        """
        self.client = client or ConversationAPIClient()
        self.parser = parser or ResponseParser()

    def enter_prompt(
        self,
        prompt: str,
        model: str = "",
        web_search: bool = False,
        provider: str = "",
        auto_continue: bool = True,
        api_key: str = None,
        chunked: bool = False  # Renamed parameter
    ) -> Union[str, Generator[str, None, None]]:
        """
        Send a prompt to the API and get the response.

        Args:
            prompt (str): The prompt to send.
            model (str): The model to use.
            web_search (bool): Whether to use web search.
            provider (str): The provider to use.
            auto_continue (bool): Whether to auto-continue.
            api_key (str): The API key to use.
            chunked (bool): Whether to return chunks or full response.

        Returns:
            Union[str, Generator[str, None, None]]: The response from the API.
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
        parsed_response = self.parser.parse_response(response, chunked)

        if not chunked:
            try:
                response.close()  # Ensure the response is closed properly
            except requests.exceptions.StreamConsumedError:
                pass
            except requests.RequestException:
                pass

        return parsed_response
