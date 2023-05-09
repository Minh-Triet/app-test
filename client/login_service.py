"""
NOTE: In context of OperationRequest and InformationRequest "user"="login".
"""

import client.proto.CMS.cmsapi_1_pb2 as cmsapi
import client.proto.CMS.common_1_pb2 as common
from client.cmsapi_client import CmsApiClient


class LoginService:
    def __init__(self, client: CmsApiClient) -> None:
        self.client = client

    async def create_login(self, login: common.User) -> str:
        """Returns ID of created login."""
        operation_request = cmsapi.OperationRequest()
        operation_request.create_user.user.CopyFrom(login)

        result = await self.client.send_operation_request(operation_request)
        return result.create_user_result.id

    async def login_info_request(self, login_id: str) -> common.User:
        information_request = cmsapi.InformationRequest()
        user_info_request = information_request.user_info_request
        user_info_request.user_id = login_id

        result = await self.client.send_information_request(information_request)
        return result.user

    async def set_login_entitlement_service(self, login_id: str, entitlementService: common.RestrictedEntitlementService) -> None:
        """Given entitlement service (product) will be either enabled or updated (if already added) for given login."""
        operation_request = cmsapi.OperationRequest()
        modify_user_entitlement_service = operation_request.modify_user_entitlement_service

        modify_user_entitlement_service.user_id = login_id
        modify_user_entitlement_service.entitlement_service_to_set.append(entitlementService)

        await self.client.send_operation_request(operation_request)

    async def update_login_settings(self, login_settings: common.LoginSettings) -> None:
        operation_request = cmsapi.OperationRequest()
        operation_request.update_login_settings.login_settings.CopyFrom(login_settings)

        await self.client.send_operation_request(operation_request)