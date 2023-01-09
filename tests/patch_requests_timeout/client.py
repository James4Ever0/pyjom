
import patchy
from requests.adapters import HTTPAdapter

REQUESTS_TIMEOUT=3 # working! great.

def patch_requests_default_timeout() -> None:
    """
    Set a default timeout for all requests made with “requests”.

    Upstream is waiting on this longstanding issue:
    https://github.com/psf/requests/issues/3070
    """

    patchy.patch(
        HTTPAdapter.send,
        f"""\
        @@ -14,6 +14,8 @@
             :param proxies: (optional) The proxies dictionary to apply to the request.
             :rtype: requests.Response
             \"""
        +    if timeout is None:
        +        timeout = {REQUESTS_TIMEOUT}

             try:
                 conn = self.get_connection(request.url, proxies)
        """,
    )

patch_requests_default_timeout()

import requests

from server import SERVER_PORT

r = requests.get(f"http://localhost:{SERVER_PORT}")