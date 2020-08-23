import logging

import quart

from bot_logging_server.models.http import requests
from bot_logging_server.models.http import headers as headers_template

logger = logging.getLogger(__name__)


async def handle(quart_request: quart.request):
    try:
        request = requests.SendLogsPostRequest.build(quart_request)
    except (KeyError, TypeError, ValueError, headers_template.WrongHeadersError) as err:
        logger.error("Request is incorrect")
        # TODO add error response
    # TODO add realization
