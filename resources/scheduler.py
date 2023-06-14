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
from models.shceduler import SchedulerManager, add_scheduler_running, update_status, \
    select_scheduler_run

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
        from main import app
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
                    if scheduler.state == 0:
                        scheduler.start()
                # scheduler.resume()
                isStart = True

                jobs = scheduler.get_jobs()
                if isStart is True and jobs is not None:
                    jobs = scheduler.get_jobs()
                    status = f'  Max instances {instance}  with interval of {time} seconds.'

            if request.form.get('Stop') == 'Remove All Jobs':
                # if isStart is False:
                # status = 'No jobs are running.'
                scheduler.remove_job('Job_1_demo')
                scheduler.remove_job('Job_2_demo')
                # lock.release()
                # with app.app_context():
                #     update_status_not_running()
                status = 'All jobs have been removed.'
                jobs = ''
                isStart = False

        except SQLAlchemyError as e:
            logger.debug(e)
            status = e

        headers = {'Content-Type': 'text/html'}

        return make_response(render_template('scheduler.html', status=status, form=form, jobs=jobs), 200, headers)


def create_scheduler():
    # from main import app

    import socket
    ip_name = socket.gethostname()
    ip_host = socket.gethostbyname(ip_name)
    if scheduler.state == 0:
        scheduler.start()
        logger.debug(f'BBBBBBBB')
    SchedulerManager.ip_address = ip_host
    SchedulerManager.status = 'Running'
    #
    id_exist = add_scheduler_running()
    time.sleep(3)
    check_id = select_scheduler_run()
    logger.debug(f'ID : {id_exist}')
    if id_exist == check_id[0]:
        job1 = scheduler.get_job('Job_1_demo')
        job2 = scheduler.get_job('Job_2_demo')
        if not job1 or not job2:
            scheduler.add_job(walk, 'interval', seconds=60, id='Job_1_demo',
                              replace_existing=True)
            scheduler.add_job(swim, 'interval', seconds=50, id='Job_2_demo',
                              replace_existing=True)
    else:
        scheduler.pause()
        update_status(id_exist)

    return id_exist
