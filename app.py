import asyncio
import atexit
import os

import nest_asyncio
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from loguru import logger
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
    logger.debug('ABCDE')
    nest_asyncio.apply()

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.message), 400

    api.add_resource(Scheduler, '/scheduler')

    return app


def run_app():
    if __name__ == '__main__':
        with app.app_context():
            id = create_scheduler()

        def cleanup():
            with app.app_context():
                update_status(id)

        atexit.register(cleanup)
        logger.debug("Running app with gunicorn")


app = create_app()
run_app()
if __name__ == '__main__':
    # run any code that you want to run only as a script here
    print("Running app as a script")
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
