import client.proto.CMS.traderouting_1_pb2 as traderouting
from client.cmsapi_client import CmsApiClient


class AccountService:
    """Methods from this class build request message (`TradeRoutingRequest`) using given message
    that represents data for particular operation (method name) and
    execute this operation in synchronous manner.
    `AccountScopeRequest` is simply a grouping message.
    """
    def __init__(self, client: CmsApiClient) -> None:
        self.client = client

    async def create_account(self, account: traderouting.Account) -> str:
        """Returns ID of created account."""
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        account_scope_request.create_account.account.CopyFrom(account)

        result = await self.client.send_traderouting_request(traderouting_request)
        return result.account_scope_result.create_account_result.id

    async def account_info_request(self, account_id: str) -> traderouting.Account:
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        account_scope_request.account_info_request.account_id = int(account_id)

        result = await self.client.send_traderouting_request(traderouting_request)
        return result.account_scope_result.account_info_result.account

    async def update_account(self, account: traderouting.Account) -> None:
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        account_scope_request.update_account.account.CopyFrom(account)

        await self.client.send_traderouting_request(traderouting_request)

    async def update_account_settings(self, account_settings: traderouting.AccountSettings) -> None:
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        account_scope_request.update_account_settings.settings.CopyFrom(account_settings)

        await self.client.send_traderouting_request(traderouting_request)

    async def account_settings_request(self, account_id: str) -> traderouting.AccountSettings:
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        account_scope_request.account_settings_request.account_id = int(account_id)

        result = await self.client.send_traderouting_request(traderouting_request)
        return result.account_scope_result.account_settings_result.account_settings

    async def update_account_risk_parameters(
        self, account_id: str, risk_parameters: traderouting.RiskParameters) -> None:
        """Do not confuse with `UpdateRiskParameters` message!"""
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        update_account_risk_parameters = account_scope_request.update_account_risk_parameters
        update_account_risk_parameters.account_id = account_id
        update_account_risk_parameters.risk_parameters.CopyFrom(risk_parameters)

        await self.client.send_traderouting_request(traderouting_request)

    async def account_risk_parameters_request(self, account_id: str) -> traderouting.RiskParameters:
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        account_scope_request.account_risk_parameters_request.account_id = int(account_id)

        result = await self.client.send_traderouting_request(traderouting_request)
        return result.account_scope_result.account_risk_parameters_result.account_risk_parameters

    async def authorize_login(self, account_user_link: traderouting.AccountUserLink) -> None:
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        account_scope_request.update_account_user_authorization_list.links_to_set.append(account_user_link)

        await self.client.send_traderouting_request(traderouting_request)

    async def authorization_list_request(self, account_id: str) -> traderouting.AccountUserAuthorizationListResult:
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        account_scope_request.account_user_authorization_list_request.account_id = int(account_id)

        result = await self.client.send_traderouting_request(traderouting_request)
        return result.account_scope_result.account_user_authorization_list_result

    async def update_account_market_limits(self, account_id: str, market_limits: traderouting.MarketLimits) -> None:
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        update_account_market_limits = account_scope_request.update_account_market_limits
        update_account_market_limits.account_id = account_id
        update_account_market_limits.market_limits.CopyFrom(market_limits)

        await self.client.send_traderouting_request(traderouting_request)

    async def account_market_limits_request(self, account_id: str) -> traderouting.MarketLimits:
        traderouting_request = traderouting.TradeRoutingRequest()
        account_scope_request = traderouting_request.account_scope_request

        account_scope_request.account_market_limits_request.account_id = int(account_id)

        result = await self.client.send_traderouting_request(traderouting_request)
        return result.account_scope_result.account_market_limits_result.account_market_limits
