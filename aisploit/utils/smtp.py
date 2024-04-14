import smtplib
import ssl as ssl_lib
from typing import Optional, Sequence, Union


class SMTPClient:
    def __init__(
        self,
        host: str,
        port: Optional[int] = None,
        ssl: bool = True,
        ssl_context: Optional[ssl_lib.SSLContext] = None,
    ) -> None:
        if not port:
            port = smtplib.SMTP_SSL_PORT if ssl else smtplib.SMTP_PORT

        self.host = host
        self.port = port
        self.ssl = ssl
        self.ssl_context = ssl_context

        self._smtp = self._create_SMTP()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._smtp.quit()

    def _create_SMTP(self) -> Union[smtplib.SMTP_SSL, smtplib.SMTP]:
        if self.ssl:
            return smtplib.SMTP_SSL(host=self.host, port=self.port, context=self.ssl_context)
        return smtplib.SMTP(host=self.host, port=self.port)

    def login(self, user: str, password: str):
        self._smtp.login(user, password)

    def sendmail(self, from_addr: str, to_addrs: str | Sequence[str], msg: str):
        self._smtp.sendmail(from_addr, to_addrs, msg)
