from loguru import logger
from sqlalchemy import text

from db import db


class SchedulerManager(db.Model):
    __tablename__ = 'SchedulerManager'
    Id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(255))
    status = db.Column(db.String(255))


def add_scheduler_running():
    global id_scheduler
    scheduler = SchedulerManager(
        ip_address=SchedulerManager.ip_address,
        status=SchedulerManager.status
    )
    try:
        db.session.add(scheduler)
        db.session.flush()
        id_scheduler = scheduler.Id
        logger.debug(id_scheduler)
        db.session.commit()
    except Exception as e:
        logger.debug(e)

    return id_scheduler


def select_scheduler_run():
    listID = []
    collects = db.session.execute(text(f"SELECT id FROM SchedulerManager WHERE status='running';"))
    for item in collects:
        listID.append(item[0])
    logger.debug(listID)
    return listID


def select_ip_run():
    listID = []
    collects = db.session.execute(text(f"SELECT ip_address FROM SchedulerManager WHERE status='running';"))
    for item in collects:
        listID.append(item['ip_address'])
    logger.debug(listID)
    return listID


def update_status(id):
    db.session.execute(text(f"UPDATE SchedulerManager set status='not running' WHERE id='{id}';"))
    db.session.commit()


def update_status_not_running():
    db.session.execute(text(f"UPDATE SchedulerManager set status='not running' WHERE status='running';"))
    db.session.commit()
