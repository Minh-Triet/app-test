import asyncio
import atexit
import os

import nest_asyncio
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from marshmallow import ValidationError
from prometheus_flask_exporter import RESTfulPrometheusMetrics

from db import db
from models.shceduler import update_status
from resources.scheduler import Scheduler, create_scheduler


def create_app():
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
    with app.app_context():
        id = create_scheduler()

    def cleanup():
        with app.app_context():
            update_status(id)
        pass

    atexit.register(cleanup)
    return app

# with app.app_context():
#     check_ip = select_ip_run()
#     scheduler.add_job(job_start, 'interval', seconds=1000, id='koko', replace_existing=True)
#     if check_ip:
#         for ip in check_ip:
#             if ip == ip_host:
#                 if scheduler.state == 0:
#                     scheduler.start()
#                     jobs1 = scheduler.get_job('Job_1_demo')
#                     jobs2 = scheduler.get_job('Job_2_demo')
#                     if not jobs1 or not jobs2:
#                         scheduler.add_job(walk, 'interval', seconds=20, id='Job_1_demo',
#                                           replace_existing=True)
#                         scheduler.add_job(swim, 'interval', seconds=30, id='Job_2_demo',
#                                           replace_existing=True)
#             else:
#                 create_scheduler()
#     else:
#         create_scheduler()
