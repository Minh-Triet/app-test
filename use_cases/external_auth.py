"""This test case demonstates setup of traderouting login that supports authentication via
external OpenID Connect provider.

1. Login into CMS API.
2. Create customer profile.
3. Create traderouting login.
4. Create an account.
5. Authorize traderouting login (step 3) to the account (step 4).
6. Enable product that supports external authentication for the login.
7. Set login specific parameters for external authentication.

To enable external authentication for a login, corresponding product (aka entitlement service) must be
enabled for this login (step 6).
This can be done only if traderouting login is authorized to an account of the brokerage (step 5).
"""

import logging
import client.proto.CMS.cmsapi_1_pb2 as cmsapi
import client.proto.CMS.common_1_pb2 as common
import client.proto.CMS.traderouting_1_pb2 as traderouting
from client.account_service import AccountService
from client.cmsapi_client import CmsApiClient
from client.profile_service import ProfileService
from client.login_service import LoginService
from development_config import Config
from .common import *


async def run(config: Config):
    print("external_auth started...")

    client = CmsApiClient()
    await client.connect(config.cms_api_url)

    logging.info("LOGIN")
    await client.send_logon(
        config.username, config.password, config.client_app_id, config.private_label, config.client_version)

    # Initialize service classes.
    account_service = AccountService(client)
    profile_service = ProfileService(client)
    login_service = LoginService(client)

    # NOTE: Steps until "ENABLE PRODUCT THAT SUPPORTS EXTERNAL AUTHENTICATION FOR THE LOGIN" can be skiped for existing login
    # that is already authorized to an account of required brokerage.

    logging.info("CREATE CUSTOMER PROFILE")

    profile = common.Profile()
    profile.legal_type = common.INDIVIDUAL
    fill_contact_information(profile.contact_information, config)
    profile.linked_brokerage_id = config.brokerage_id

    profile_id = await profile_service.create_profile(profile)

    logging.info("CREATE TRADEROUTING LOGIN")

    # In this context "user"="login".
    login = common.User()
    login.user_name = generate_name(config.brokerage_id, 32)
    login.subscriber_type = common.User.PRO
    login.domain = common.CQG_TRADE_ROUTING
    login.profile_id = profile_id

    login_id = await login_service.create_login(login)

    logging.info("CREATE ACCOUNT")

    # One of "required-create" field is `account_type_id`.
    # List of available values for this field can be obtained using next request.
    account = traderouting.Account()
    account.name = generate_name(config.brokerage_id, 64)
    account.brokerage_account_number = generate_name(config.brokerage_id, 12)
    # `class` is reserved keyword in Python.
    setattr(account, "class", traderouting.Account.Class.REGULAR)
    account.account_type_id = "0"  # N/A. See account_setup for details.
    account.profile_id = profile_id
    account.profile_sales_series_id = config.profile_sales_series_id

    account_id = await account_service.create_account(account)

    logging.info("AUTHORIZE LOGIN TO THE ACCOUNT")

    # "user"="login"
    account_user_link = traderouting.AccountUserLink()
    account_user_link.account_id = int(account_id)
    account_user_link.user_id = login_id

    await account_service.authorize_login(account_user_link)

    logging.info(
        "ENABLE PRODUCT THAT SUPPORTS EXTERNAL AUTHENTICATION FOR THE LOGIN")

    # NOTE: It is expected that given brokerage is already authorized to such product,
    # so product ID (aka entitlement service ID) is provided by CQG.
    entitlementService = common.RestrictedEntitlementService()
    entitlementService.entitlement_service_id = config.external_auth_service_id
    assigned_brokerage = common.AssignedBrokerage()
    assigned_brokerage.brokerage_id = config.brokerage_id
    entitlementService.assigned_brokerages.append(assigned_brokerage)

    await login_service.set_login_entitlement_service(login_id, entitlementService)

    logging.info("SET LOGIN SPECIFIC PARAMETERS FOR EXTERNAL AUTHENTICATION")

    login_settings = common.LoginSettings()
    login_settings.login_id = login_id
    # ID of external authentication partner. Provided by CQG.
    login_settings.external_auth.partner_id = config.external_auth_partner_id
    # Username as registered by authentication partner.
    login_settings.external_auth.username = generate_name(config.brokerage_id, 255)

    await login_service.update_login_settings(login_settings)

    await client.disconnect()
    print("external_auth finished.")
