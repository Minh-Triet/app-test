import asyncio
import os

import nest_asyncio
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from marshmallow import ValidationError
from prometheus_flask_exporter import RESTfulPrometheusMetrics

import ma
from db import db
from resources.cmsapi import CmsApi
from resources.customer import Customer, CustomerList, CustomerDetail
from resources.scheduler import Scheduler
from resources.trade import Trade, TradeList, TradeDetail
from resources.trade_cqg import TradeCQG

app = Flask(__name__)
load_dotenv('.env.example', verbose=True)
app.config.from_object('development_config')  # load default configs from development_config.py
app.config.from_envvar('APPLICATION_SETTING')  # override with config.py (APPLICATION_SETTINGS points to config.py)

api = Api(app)
migrate = Migrate(app, db)
db.init_app(app)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(asyncio.new_event_loop())
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
metrics = RESTfulPrometheusMetrics(app, api)

# metrics.info("app_info", "App Info, this can be anything you want", version="1.0.0")

nest_asyncio.apply()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.message), 400


api.add_resource(Trade, '/trades')
api.add_resource(TradeDetail, '/trade/<int:_id>')
api.add_resource(TradeList, '/trades')
api.add_resource(Customer, '/customer')
api.add_resource(CustomerDetail, '/customer/<int:_id>')
api.add_resource(CustomerList, '/customers')
api.add_resource(TradeCQG, '/cqg')
api.add_resource(CmsApi, '/cmsapi')
api.add_resource(Scheduler, '/scheduler')

import requests

# a = requests.get('http://127.0.0.1:5000/cqg')
# print(a.text)
# # proxies = {'http': 'user:pass@10.10.10.10'}
#
# r = requests.get('wss://democmsapi.cqg.com:443')
#
# print(f'Status Code: {r.status_code}')

# ws = websocket.WebSocket()
# ws.connect("wss://democmsapi.cqg.com:443", http_proxy_host="192.168.95.100", http_proxy_port=3128)
# var = ws.recv()
# print(var)

# ws = websocket.WebSocket()
# ws.connect("ws://democmsapi.cqg.com:443",
#            http_proxy_host="192.168.95.100", http_proxy_port="3128",
#            proxy_type="http")
# ws.send("Hello, Server")
# print(ws.recv())
# ws.close()


if __name__ == '__main__':
    ma.ma.init_app(app)
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
