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
from development_config import scheduler, redis
from resources.scheduler import Scheduler, swim, walk

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


api.add_resource(Scheduler, '/scheduler')

# def create_scheduler():
#     if scheduler.state == 0:
#         scheduler.start()
#
#     SchedulerManager.ip_address = ip_host
#     SchedulerManager.status = 'Running'
#     id_exist = add_scheduler_running()
#     time.sleep(3)
#     check_id = select_scheduler_run()
#
#     if check_id[0] == id_exist:
#         jobs = scheduler.get_jobs()
#         if not jobs:
#             scheduler.add_job(walk, 'interval', seconds=20, id='Job_1_demo',
#                               replace_existing=True)
#
#             scheduler.add_job(swim, 'interval', seconds=30, id='Job_2_demo',
#                               replace_existing=True)
#     else:
#         scheduler.shutdown()
#         update_status(id_exist)
#
#
# # import socket
# #
# # ip_name = socket.gethostname()
# # ip_host = socket.gethostbyname(ip_name)
# #
# # with app.app_context():
# #     check_ip = select_ip_run()
# #     if check_ip:
# #         for ip in check_ip:
# #             if ip == ip_host:
# #                 scheduler.start()
# #             else:
# #                 create_scheduler()
# #     else:
# #         create_scheduler()
lock = redis.lock('api-test', 180)
if lock.acquire(blocking=False):
    if scheduler.state == 0:
        scheduler.start()
        jobs = scheduler.get_jobs()
        if not jobs:
            scheduler.add_job(walk, 'interval', seconds=20, id='Job_1_demo',
                              replace_existing=True)

            scheduler.add_job(swim, 'interval', seconds=30, id='Job_2_demo',
                              replace_existing=True)

if __name__ == '__main__':
    ma.ma.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
