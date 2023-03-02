from __future__ import annotations

import re

from starlette.datastructures import URL
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send

repeated_quotes = re.compile(r'//+')


class HttpUrlRedirectMiddleware:
  """
  This http middleware redirects urls with repeated slashes to the cleaned up
  versions of the urls
  """

  def __init__(self, app: ASGIApp) -> None:
    self.app = app

  async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

    if scope["type"] == "http" and repeated_quotes.search(URL(scope=scope).path):
      url = URL(scope=scope)
      url = url.replace(path=repeated_quotes.sub('/', url.path))
      response = RedirectResponse(url, status_code=307)
      await response(scope, receive, send)
    else:
      await self.app(scope, receive, send)