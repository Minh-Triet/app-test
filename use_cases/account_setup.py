"""Demonstrates how trading account can be set up via CMS API.
[demo] indicates that this step does not make much sense in real use case.
Demonstrates how trading account can be set up vie CMS API.
[demo] indicates that this step does not make much sense in real use case.
"""

import json
import logging

import pandas

from loguru import logger

import client.proto.CMS.traderouting_1_pb2 as trade_routing

from client.cmsapi_client import CmsApiClient
from .common import *

# Random number that is used as value when setting limits.


async def run(config: Config):
    logger.debug("account_setup started...")
    client = CmsApiClient()
    await client.connect(config.cms_api_url)

    logging.info("LOGON")
    await client.send_logon(
        config.username, config.password, config.client_app_id, config.private_label, config.client_version)

    # create balance record
    # account_balance = traderouting.TradeRoutingRequest()
    # balance = account_balance.account_scope_request
    # acc = balance.create_balance_record
    # acc.account_id = 17093758
    # acc.currency = 'VND'
    # acc.end_cash_balance = 0
    # await client.send_traderouting_request(account_balance)
    # logger.debug(balance_record)

    # # update balance record
    # account_balance = traderouting.TradeRoutingRequest()
    # balance = account_balance.account_scope_request
    # acc = balance.update_balance_record
    # acc.balance_id = 328836621
    # acc.end_cash_balance = 999999
    # balance_record = await client.send_traderouting_request(account_balance)
    # logger.debug(balance_record)

    account_balance = trade_routing.TradeRoutingRequest()
    balance = account_balance.account_scope_request
    acc = balance.balance_records_request
    # acc.balance_id = 321009136
    # acc.currency = 'USDC'
    acc.account_id = 17093758
    balance_record = await client.send_traderouting_request(account_balance)

    # class data:
    #     def _init_(self):
    #         self.account_id: 17093758
    #         self.balance_record_id: 321009136
    #         self.currency: "CNY"
    #         self.end_cash_balance: 125558.0
    #         self.collateral: 0.0
    #         self.as_of_date: 1669766400000
    #         self.origin: 1
    #         self.regulated: true
    from google.protobuf.json_format import MessageToJson
    json_str = MessageToJson(balance_record)
    logger.debug(json_str)
    json_dct = json.loads(json_str)
    account_id = json_dct['accountScopeResult']['balanceRecordsResult']['balanceRecord'][0]['accountId']
    balance_record_id = json_dct['accountScopeResult']['balanceRecordsResult']['balanceRecord'][0][
        'balanceRecordId']
    end_cash_balance = json_dct['accountScopeResult']['balanceRecordsResult']['balanceRecord'][0]['currency']
    currency = json_dct['accountScopeResult']['balanceRecordsResult']['balanceRecord'][0]['endCashBalance']
    collateral = json_dct['accountScopeResult']['balanceRecordsResult']['balanceRecord'][0]['collateral']
    time_ms = json_dct['accountScopeResult']['balanceRecordsResult']['balanceRecord'][0]['asOfDate']
    as_of_date = pandas.to_datetime(time_ms, unit='ms')
    origin = json_dct['accountScopeResult']['balanceRecordsResult']['balanceRecord'][0]['origin']
    regulated = json_dct['accountScopeResult']['balanceRecordsResult']['balanceRecord'][0]['regulated']
    # Not - available.
    # NA = 1;
    # Local
    # LOCAL = 2;
    # // Abroad
    # OVERSEAS = 3;
    logger.debug(account_id)
    logger.debug(balance_record_id)
    logger.debug(end_cash_balance)
    logger.debug(currency)
    logger.debug(collateral)
    logger.debug(as_of_date)
    logger.debug(origin)
    logger.debug(regulated)

    await client.disconnect()
    logger.debug("account_setup finished.")
