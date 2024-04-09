from typing import Optional, List
import time
from dataclasses import dataclass
import email
from email import policy
from email.mime.text import MIMEText
from imapclient import IMAPClient
import ssl as ssl_lib

from ..core import BaseTarget, BasePromptValue
from ..utils import SMTPClient


@dataclass(frozen=True)
class UserPasswordAuth:
    user: str
    password: str


@dataclass(frozen=True)
class EmailSender:
    host: str
    auth: UserPasswordAuth
    port: Optional[int] = None
    ssl: bool = True
    ssl_context: Optional[ssl_lib.SSLContext] = None

    def send_email(self, from_addr: str, to_addr: str, subject: str, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_addr

        with SMTPClient(self.host, self.port) as client:
            client.login(self.auth.user, self.auth.password)
            client.sendmail(from_addr, to_addr, msg.as_string())


@dataclass(frozen=True)
class EmailReceiver:
    host: str
    auth: UserPasswordAuth
    port: Optional[int] = None
    folder: str = "INBOX"
    ssl: bool = True
    ssl_context: Optional[ssl_lib.SSLContext] = None

    def listen_for_emails(self, from_addr: str, timeout=None) -> List[str]:
        start_time = time.time()
        with IMAPClient(
            host=self.host, port=self.port, ssl=self.ssl, ssl_context=self.ssl_context
        ) as client:
            client.login(self.auth.user, self.auth.password)
            client.select_folder(self.folder, readonly=True)
            client.idle()

            emails = []
            while True:
                elapsed_time = time.time() - start_time
                if timeout is not None and elapsed_time >= timeout:
                    break  # Exit the loop if the timeout has elapsed

                response = client.idle_check(
                    timeout=(
                        min(30, timeout - elapsed_time) if timeout is not None else None
                    )
                )

                if response:
                    client.idle_done()

                    messages = client.search(["UNSEEN", "FROM", from_addr])

                    for _, msg_data in client.fetch(messages, "RFC822").items():
                        msg = email.message_from_bytes(
                            msg_data[b"RFC822"], policy=policy.default
                        )

                        sender = msg["From"]
                        subject = msg["Subject"]
                        body = None

                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                if content_type == "text/plain":
                                    body = part.get_payload(decode=True)
                        else:
                            body = msg.get_payload(decode=True)

                        if isinstance(body, bytes):
                            body = body.decode("utf-8")

                        emails.append(
                            f"From: {sender}\nSubject: {subject}\nBody: {body}\n"
                        )

                    if len(emails) > 0:
                        break

            return emails


class EmailTarget(BaseTarget):
    def __init__(
        self,
        *,
        sender: EmailSender,
        receiver: EmailReceiver,
        subject: str,
        from_addr: str,
        to_addr: str,
    ) -> None:
        self._sender = sender
        self._receiver = receiver
        self._subject = subject
        self._from_addr = from_addr
        self._to_addr = to_addr

    def send_prompt(self, prompt: BasePromptValue) -> str:
        self._sender.send_email(
            from_addr=self._from_addr,
            to_addr=self._to_addr,
            subject=self._subject,
            body=prompt.to_string(),
        )

        emails = self._receiver.listen_for_emails(
            from_addr=self._from_addr, timeout=120
        )

        return "\n".join(emails)
