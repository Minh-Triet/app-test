import asyncio
from flask_restful import Resource

import datetime
import logging
from authentication import auth
from development_config import Config
from use_cases import account_setup, external_auth

_use_case_map = {
    'account_setup': account_setup,
    'external_auth': external_auth
}


class CmsApi(Resource):
    @classmethod
    @auth.login_required()
    async def get(cls):
        # logging.basicConfig(
        #     filename=f'./logs/account_setup--{datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}.log',
        #     filemode='w', encoding='utf-8', level=logging.DEBUG)
        config = Config()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_use_case_map['account_setup'].run(config))
        return "hello"
