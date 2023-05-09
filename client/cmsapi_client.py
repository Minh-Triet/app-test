import datetime
import logging
import ssl
from typing import Dict, List

import websockets
from google.protobuf.message import Message

from .proto.CMS import cmsapi_1_pb2 as cmsapi
from .proto.CMS import common_1_pb2 as common
from .proto.CMS import traderouting_1_pb2 as traderouting
from .proto.common import shared_1_pb2 as shared


class CmsError(Exception):
    """Represents an error from CMS API."""

    def __init__(self, error_message: shared.Text) -> None:
        super().__init__(error_message.text)

        # Any error from the API is passed inside shared_1.Text object.
        # It contains error code, error text and sometimes additional parameters.
        self.error_message = error_message


class CmsApiClient:
    """Provides high-level interface over CMS API operations.
    Demonstrates best practices of working with CMS API.

    Methods like `send_information_request` allows to work with API in synchronous manner -
    send one message and wait until result is received, then send one more message etc.

    `send_client_message` and `wait_for_result` allow to work with API asynchronously
    by sending batch of requests in single `client_message` and then waiting for results (separately) whenever it is needed.
    """

    def __init__(self) -> None:
        self._socket = None

        self._logon_result: common.LogonResult = None

        self._unprocessed_results: Dict[str, List[Message]] = dict([])
        self._unprocessed_results[cmsapi.InformationRequest.DESCRIPTOR.full_name] = []
        self._unprocessed_results[cmsapi.SearchRequest.DESCRIPTOR.full_name] = []
        self._unprocessed_results[cmsapi.OperationRequest.DESCRIPTOR.full_name] = []
        self._unprocessed_results[traderouting.TradeRoutingRequest.DESCRIPTOR.full_name] = []

        self._last_request_id = 0

        # Configure logger of websockets library.
        logger = logging.getLogger("websockets")
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())

    async def connect(self, uri: str) -> None:
        await self.disconnect()
        self._socket = await websockets.connect(uri=uri)
        logging.info(f"Connected to {uri}")

    async def disconnect(self) -> None:
        if self._socket and not self._socket.closed:
            await self._socket.close()
            logging.info(f"Disconnected")

    async def send_client_message(
            self, client_message: cmsapi.ClientMessage, expect_response: bool = True) -> None:
        """Sends the message to API.
        CMS API does not guarantee that requests will be answered in the same order in which they were sent.
        """
        data = client_message.SerializeToString()
        await self._socket.send(data)
        logging.info(f"Message out:\n{client_message}")

    async def receive_server_message(self) -> None:
        """Get message from incoming message queue."""
        data = await self._socket.recv()

        # Deserialize message.
        server_message = cmsapi.ServerMessage()
        server_message.ParseFromString(data)
        logging.info(f"Message in:\n{server_message}")

        if server_message.HasField("ping"):
            await self.send_pong(server_message.ping)

        # Get all "result" messages from received message.
        # ServerMessage itself is basically container
        # in which several requests of different type can be combined.
        if server_message.HasField("logon_result"):
            self._logon_result = server_message.logon_result
            return  # logon_result always comes alone.

        for result in server_message.information_result:
            self._unprocessed_results[cmsapi.InformationRequest.DESCRIPTOR.full_name].append(result)

        for result in server_message.search_result:
            self._unprocessed_results[cmsapi.SearchRequest.DESCRIPTOR.full_name].append(result)

        for result in server_message.operation_result:
            self._unprocessed_results[cmsapi.OperationRequest.DESCRIPTOR.full_name].append(result)

        for result in server_message.trade_routing_result:
            self._unprocessed_results[traderouting.TradeRoutingRequest.DESCRIPTOR.full_name].append(result)

    async def wait_for_result(self, request: Message) -> Message:
        """Awaits for result of given request message.
        Matched result message is calculated from given request message.
        First, it looks into list of received unprocessed messages (because messages can come in any order and/or grouped)
        and then if message is not found it awaits for new messages from server.
        """
        result = None

        while not result:
            if isinstance(request, common.Logon):
                # There can be only one LogonRequest and LogonResult in scope of one session.
                result = self._logon_result
                self._logon_result = None

            elif type(request) in [
                cmsapi.InformationRequest, cmsapi.SearchRequest,
                cmsapi.OperationRequest, traderouting.TradeRoutingRequest]:

                results = self._unprocessed_results[request.DESCRIPTOR.full_name]
                result = next((r for r in results if r.request_id == request.id), None)
                if result:
                    results.remove(result)

            if not result:
                # If result has not been received yet, wait for new messages from server.
                await self.receive_server_message()

        return result

    async def send_pong(self, ping: Message) -> None:
        client_message = cmsapi.ClientMessage()
        pong = client_message.pong
        pong.token = ping.token
        pong.ping_utc_time = ping.ping_utc_time
        pong.pong_utc_time = datetime.datetime.utcnow().timestamp()

        await self.send_client_message(client_message)

    async def send_logon(
            self, username: str, password: str, client_app_id: str, private_label: str, client_version: str) -> Message:
        """Authenticates current session. This is mandatory to start working with CMS API."""
        client_message = cmsapi.ClientMessage()
        logon: common.Logon = client_message.logon

        # These 2 fields indicate what protocol version is used by the client.
        logon.protocol_version_minor = cmsapi.PROTOCOL_VERSION_MINOR
        logon.protocol_version_major = cmsapi.PROTOCOL_VERSION_MAJOR

        logon.user_name = username
        logon.password = password
        logon.client_app_id = client_app_id
        logon.private_label = private_label
        logon.client_version = client_version

        await self.send_client_message(client_message)
        logon_result = await self.wait_for_result(logon)

        if logon_result.operation_status == common.FAILURE:
            raise CmsError(logon_result.error_message)

        return logon_result

    async def send_information_request(self, information_request: Message) -> Message:
        return await self._send_request(
            information_request, lambda client_message: client_message.information_request)

    async def send_search_request(self, search_request: Message) -> Message:
        return await self._send_request(
            search_request, lambda client_message: client_message.search_request)

    async def send_operation_request(self, operation_request: Message) -> Message:
        return await self._send_request(
            operation_request, lambda client_message: client_message.operation_request)

    async def send_traderouting_request(self, traderouting_request: Message) -> Message:
        return await self._send_request(
            traderouting_request, lambda client_message: client_message.trade_routing_request)

    async def _send_request(self, request: Message, request_collection_getter) -> Message:
        # Make sure that ID of the request is unique in scope of one session.
        # Requests of different types can have the same ID.
        if not request.HasField("id"):
            request.id = self._get_request_id()

        client_message: Message = cmsapi.ClientMessage()
        request_collection_getter(client_message).append(request)

        await self.send_client_message(client_message)
        result = await self.wait_for_result(request)

        if result.operation_status != common.SUCCESS:
            raise CmsError(result.error_message)

        return result

    def _get_request_id(self):
        self._last_request_id += 1
        return self._last_request_id
