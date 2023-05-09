import client.proto.CMS.cmsapi_1_pb2 as cmsapi
import client.proto.CMS.common_1_pb2 as common
from client.cmsapi_client import CmsApiClient


class ProfileService:
    def __init__(self, client: CmsApiClient) -> None:
        self.client = client

    async def create_profile(self, profile: common.Profile) -> str:
        """Returns ID of created profile."""
        operation_request = cmsapi.OperationRequest()

        operation_request.create_profile.profile.CopyFrom(profile)

        result = await self.client.send_operation_request(operation_request)
        return result.create_profile_result.profile_id

    async def profile_request(self, profile_id: str) -> common.Profile:
        information_request = cmsapi.InformationRequest()

        profile_request = information_request.profile_request
        profile_request.profile_id = profile_id

        result = await self.client.send_information_request(information_request)
        return result.profile
