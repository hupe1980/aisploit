import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Literal
from urllib import parse

import websocket
from requests.sessions import Session

from ..core import BasePromptValue, BaseTarget, Response
from ..utils import cookies_as_dict

BUNDLE_VERSION = "1.1690.0"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36"

CREATE_HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://copilot.microsoft.com/",
    "Sec-Ch-Ua": '"Chromium";v="123", "Not:A-Brand";v="8"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "macOS",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": USER_AGENT,
}

CHATHUB_HEADERS = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "Upgrade",
    "Origin": "https://copilot.microsoft.com",
    "Pragma": "no-cache",
    "User-Agent": USER_AGENT,
}

BING_CREATE_CONVERSATION_URL = "https://copilot.microsoft.com/turing/conversation/create"

BING_CHATHUB_URL = "wss://sydney.bing.com/sydney/ChatHub"

DELIMETER = "\x1e"  # Record separator character.

_conversation_style_option_sets = {
    "creative": ["h3imaginative", "clgalileo", "gencontentv3"],
    "balanced": ["galileo"],
    "precise": ["h3precise", "clgalileo"],
}


@dataclass
class CopilotTarget(BaseTarget):
    """
    A class representing the target for sending prompts to Copilot.
    """

    conversation_style: Literal["balanced", "creative", "precise"] = "balanced"
    bing_cookies: str | None = None
    bundle_version: str = BUNDLE_VERSION

    def send_prompt(self, prompt: BasePromptValue) -> Response:
        """
        Send a prompt to Copilot and receive the response.

        Args:
            prompt (BasePromptValue): The prompt value to send.

        Returns:
            Response: The response received from Copilot.
        """
        with CopilotClient(
            conversation_style=self.conversation_style,
            bing_cookies=self.bing_cookies,
        ) as client:
            response = client.create_completion(prompt.to_string())
            return Response(content=response["text"])


@dataclass(kw_only=True)
class CopilotClient:
    """
    A class representing the client for interacting with Copilot.
    """

    conversation_style: Literal["balanced", "creative", "precise"] = "balanced"
    bing_cookies: str | None = None
    bundle_version: str = BUNDLE_VERSION

    session: Session | None = field(default=None, init=False)
    ws_connection: websocket.WebSocket | None = field(default=None, init=False)
    conversation_id: str | None = field(default=None, init=False)
    conversation_signature: str | None = field(default=None, init=False)
    client_id: str | None = field(default=None, init=False)
    invocation_id: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if not self.bing_cookies:
            self.bing_cookies = os.getenv("BING_COOKIES")

    def __enter__(self):
        self.start_conversation()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_conversation()

    def start_conversation(self) -> None:
        """
        Start a conversation with Copilot.
        """
        session = self._get_session(force_close=True)

        response = session.get(f"{BING_CREATE_CONVERSATION_URL}?bundleVersion={self.bundle_version}")
        response.raise_for_status()

        response_dict = response.json()
        if response_dict["result"]["value"] != "Success":
            raise ValueError(f"Failed to authenticate, received message: {response_dict['result']['message']}")

        self.conversation_id = response_dict["conversationId"]
        self.client_id = response_dict["clientId"]
        self.conversation_signature = response.headers["X-Sydney-Conversationsignature"]
        self.encrypted_conversation_signature = response.headers["X-Sydney-Encryptedconversationsignature"]

        self.invocation_id = 0

    def close_conversation(self) -> None:
        """
        Close the conversation with Copilot.
        """
        if self.ws_connection:
            self.ws_connection.close()
            self.ws_connection = None

        if self.session:
            self.session.close()
            self.session = None

    def create_completion(
        self,
        prompt: str,
        search: bool = True,
        raw: bool = False,
    ) -> Dict[str, Any]:
        """
        Create a completion request and interact with Copilot.

        Args:
            prompt (str): The prompt to send to Copilot.
            search (bool, optional): Whether to allow search. Defaults to True.
            raw (bool, optional): Whether to return raw response. Defaults to False.

        Returns:
            Dict[str, Any]: The response received from Copilot.
        """
        bing_chathub_url = BING_CHATHUB_URL
        if self.encrypted_conversation_signature:
            bing_chathub_url += f"?sec_access_token={parse.quote(self.encrypted_conversation_signature)}"

        self.ws_connection = websocket.create_connection(bing_chathub_url, extra_headers=CHATHUB_HEADERS, max_size=None)

        assert self.ws_connection is not None, "ws_connection should not be None"

        self.ws_connection.send(as_json({"protocol": "json", "version": 1}))

        self.ws_connection.recv()

        request = self._build_arguments(prompt, search)

        self.invocation_id += 1

        self.ws_connection.send(as_json(request))

        while True:
            objects = str(self.ws_connection.recv()).split(DELIMETER)
            for obj in objects:
                if not obj:
                    continue
                response = json.loads(obj)

                # Ignore type 1 messages (streaming).
                if response.get("type") == 1:
                    continue
                # Handle type 2 messages.
                elif response.get("type") == 2:
                    # Check if reached conversation limit.
                    if response["item"].get("throttling"):
                        number_of_messages = response["item"]["throttling"].get("numUserMessagesInConversation", 0)
                        max_messages = response["item"]["throttling"]["maxNumUserMessagesInConversation"]
                        if number_of_messages == max_messages:
                            raise ValueError(f"Reached conversation limit of {max_messages} messages")

                    messages = response["item"].get("messages")
                    if not messages:
                        result_value = response["item"]["result"]["value"]
                        if result_value == "Throttled":
                            raise ValueError("Request is throttled")
                        elif result_value == "CaptchaChallenge":
                            raise ValueError("Solve CAPTCHA challenge to continue")
                        else:
                            raise ValueError(f"Unknown result value: '{result_value}'")

                    if raw:
                        return response
                    else:
                        i = -1
                        adaptiveCards = messages[-1].get("adaptiveCards")
                        if adaptiveCards and adaptiveCards[-1]["body"][0].get("inlines"):
                            # Adjust the index in situations where the last message
                            # is an inline message, which often happens when an
                            # attachment is included.
                            i = -2
                        return messages[i]

    def _get_session(self, force_close: bool = False) -> Session:
        """
        Get a requests session.

        Args:
            force_close (bool, optional): Whether to force close the session. Defaults to False.

        Returns:
            Session: The requests session.
        """
        cookies = cookies_as_dict(self.bing_cookies) if self.bing_cookies else {}

        if self.session and force_close:
            self.session.close()
            self.session = None

        if not self.session:
            self.session = Session()
            self.session.headers.update(CREATE_HEADERS)
            self.session.cookies.update(cookies)

        return self.session

    def _build_arguments(
        self,
        prompt: str,
        search: bool,
    ) -> dict:
        """
        Build arguments for the completion request.

        Args:
            prompt (str): The prompt to send.
            search (bool): Whether to allow search.

        Returns:
            dict: The arguments for the completion request.
        """
        options_sets = [
            "nlu_direct_response_filter",
            "deepleo",
            "disable_emoji_spoken_text",
            "responsible_ai_policy_235",
            "enablemm",
            "dv3sugg",
            "iyxapbing",
            "iycapbing",
            "saharagenconv5",
            "eredirecturl",
        ]

        options_sets.extend(_conversation_style_option_sets[self.conversation_style])

        if self.bing_cookies:
            options_sets.extend("autosave")

        if not search:
            options_sets.extend("nosearchall")

        arguments: dict = {
            "arguments": [
                {
                    "source": "cib",
                    "optionsSets": options_sets,
                    "allowedMessageTypes": [
                        "ActionRequest",
                        "Chat",
                        "ConfirmationCard",
                        "Context",
                        "InternalSearchQuery",
                        "InternalSearchResult",
                        "Disengaged",
                        "InternalLoaderMessage",
                        "Progress",
                        "RenderCardRequest",
                        "RenderContentRequest",
                        "AdsQuery",
                        "SemanticSerp",
                        "GenerateContentQuery",
                        "SearchQuery",
                        "GeneratedCode",
                        "InternalTasksMessage",
                        "Disclaimer",
                    ],
                    "sliceIds": [],
                    "verbosity": "verbose",
                    "scenario": "SERP",
                    "plugins": [],
                    "conversationHistoryOptionsSets": ["autosave", "savemem", "uprofupd", "uprofgen"],
                    "gptId": "copilot",
                    "isStartOfSession": self.invocation_id == 0,
                    "message": {
                        "author": "user",
                        "inputMethod": "Keyboard",
                        "text": prompt,
                        "messageType": "Chat",
                        "imageUrl": None,
                        "originalImageUrl": None,
                    },
                    "conversationSignature": self.conversation_signature,
                    "participant": {
                        "id": self.client_id,
                    },
                    "tone": self.conversation_style.title(),
                    "spokenTextMode": "None",
                    "conversationId": self.conversation_id,
                }
            ],
            "invocationId": str(self.invocation_id),
            "target": "chat",
            "type": 4,
        }

        return arguments


def as_json(message: dict) -> str:
    """
    Convert a dictionary to a JSON string and append a delimiter.

    Args:
        message (dict): The dictionary to convert.

    Returns:
        str: The JSON string with delimiter appended.
    """
    return json.dumps(message) + DELIMETER
