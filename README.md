# AI-Based Conversation API Client

This Python module provides a powerful and flexible interface for interacting with an AI-based conversation API. It enables users to seamlessly send prompts and receive intelligent responses from a specified API endpoint, with robust support for both full and chunked responses.

## Key Features

- Easy-to-use interface for sending prompts and receiving AI-generated responses
- Support for both full and chunked response modes for real-time interaction
- Customizable API client and response parser for flexibility
- Configurable options for AI model selection and parameters

## Installation

To install the AI-Based Conversation API Client, follow these steps:

1. Clone the repository or download the source code:
   ```
   git clone https://github.com/Muhammadali-Akbarov/ai-conversation-api-client.git
   ```
   or download and extract the ZIP file from the repository's main page.

2. Navigate to the project directory:
   ```
   cd ai-conversation-api-client
   ```

3. Run the installation script:
   ```
   ./install.sh
   ```

After running the installation script, your environment will be fully set up and ready to use the AI-Based Conversation API Client.

## Usage Example

Here's a simple example of how to use the AI-Based Conversation API Client:

```python
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
```

Result
```
Sure! Here are ten programming languages:

1. Python
2. Java
3. JavaScript
4. C++
5. C#
6. Ruby
7. PHP
8. Swift
9. Go
10. Rust

Let me know if you need more information about any of these languages!
