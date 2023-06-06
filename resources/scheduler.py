import time
from datetime import datetime

from flask import make_response, render_template, request
from flask_restful import Resource
from flask_wtf import FlaskForm
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange

from development_config import scheduler
from models.shceduler import update_status_not_running

isStart = False


def walk():
    logger.debug(datetime.now())
    logger.debug(scheduler.state)

def swim():
    for a in range(30):
        time.sleep(1)
        logger.debug(a)


class MyForm(FlaskForm):
    instance = IntegerField('Max instances:', validators=[DataRequired(), NumberRange(min=1)])
    time = IntegerField('Interval (seconds):', validators=[DataRequired(), NumberRange(min=0)])


class Scheduler(Resource):
    @classmethod
    def get(cls):

        form = MyForm()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('scheduler.html', form=form), 200, headers)

    @classmethod
    def post(cls):
        global isStart, status, jobs
        from app import app
        with app.app_context():
            form = MyForm()
        try:
            if request.form.get('Start') == 'Start':
                jobs = ''
                instance = request.form.get('instance')
                time = request.form.get('time')

                if isStart is False:
                    scheduler.add_job(walk, 'interval', seconds=int(time), id='Job_1_demo',
                                      replace_existing=True)

                    scheduler.add_job(swim, 'interval', seconds=int(time), id='Job_2_demo',
                                      replace_existing=True)

                    scheduler.start()

                isStart = True

                jobs = scheduler.get_jobs()
                if isStart is True and jobs is not None:
                    jobs = scheduler.get_jobs()
                    status = f'  Max instances {instance}  with interval of {time} seconds.'

            if request.form.get('Stop') == 'Remove All Jobs':
                # if isStart is False:
                # status = 'No jobs are running.'
                scheduler.resume_job('Job_1_demo')
                scheduler.resume_job('Job_2_demo')
                # lock.release()
                with app.app_context():
                    update_status_not_running()
                status = 'All jobs have been removed.'
                jobs = ''
                isStart = False

        except SQLAlchemyError as e:
            logger.debug(e)
            status = e

        headers = {'Content-Type': 'text/html'}

        return make_response(render_template('scheduler.html', status=status, form=form, jobs=jobs), 200, headers)
