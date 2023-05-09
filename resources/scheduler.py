from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask import make_response, render_template, request
from flask_restful import Resource
from flask_wtf import FlaskForm
from loguru import logger
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange

isStart = False


def walk():
    print(datetime.now())


def swim():
    print('demo2')


class MyForm(FlaskForm):
    instance = IntegerField('Max instances:', validators=[DataRequired(), NumberRange(min=1)])
    time = IntegerField('Interval (seconds):', validators=[DataRequired(), NumberRange(min=0)])


class Scheduler(Resource):
    @classmethod
    def get(cls):
        from app import app
        with app.app_context():
            form = MyForm()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('scheduler.html', form=form), 200, headers)

    @classmethod
    def post(cls):
        global isStart, scheduler, status, jobs
        from app import app
        with app.app_context():
            form = MyForm()
        try:
            if request.form.get('Start') == 'Start':
                instance = request.form.get('instance')
                time = request.form.get('time')
                jobstores = {
                    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
                }

                executors = {
                    'default': ThreadPoolExecutor(20),
                    'processpool': ProcessPoolExecutor(5)
                }
                job_defaults = {
                    'coalesce': False,
                    'max_instances': instance
                }
                if isStart is False:
                    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors,
                                                    job_defaults=job_defaults, timezone='Asia/ho_chi_minh')

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
                if isStart is False:
                    status = 'No jobs are running.'
                    jobs = ''
                elif isStart is True:
                    scheduler.remove_all_jobs()
                    status = 'All jobs have been removed.'
                    jobs = ''
                    scheduler.shutdown()
                    isStart = False

        except BaseException as e:
            logger.debug(e)
            status = e

        headers = {'Content-Type': 'text/html'}

        return make_response(render_template('scheduler.html', status=status, form=form, jobs=jobs), 200, headers)
