import logging
import sys
# import amb
import datetime

from authentication import auth
from db import db
from loguru import logger
from constants.amb_server import ambAddress, writer_name, trade_subject

writer_id = 0
reader_id = 0
check_loop = 0


def reply_cb(message, status, arg):
    logger.debug('Reply from AMB server:...')
    buf = amb.mbf_create_buffer_from_data(message.data_p)
    message_from_amb = buf.mbf_read()

    date_now = datetime.datetime.now()
    TradeModel.LastModification = date_now
    TradeModel.ResponseFromAMB = message_from_amb.mbf_object_to_string_xml()
    global check_loop
    logging.debug(f'check_loop before =  {check_loop}')
    check_loop = 1
    logging.debug(f'check_loop after refreshing =  {check_loop}')


def message_sent_cb(channel, event, arg):
    event_string = amb.mb_event_type_to_string(event.event_type)
    logger.debug(f'event: {event_string}')

    if event_string == 'Status':
        try:
            logger.debug("event.status.status = ", event.status.status, type(event.status.status))
            amb_msg_nbr = int(event.status.status)
            logger.debug(amb_msg_nbr)
        except ValueError:
            amb_msg_nbr = 0

    elif event_string == 'Disconnect':
        logger.debug(f'Disconnected to AMB server...')

    elif event_string == 'Async':
        logger.debug("Async")


class TradeModel(db.Model):
    __tablename__ = 'TradeTransaction'

    Id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    type = db.Column(db.NVARCHAR(255))
    time = db.Column(db.NVARCHAR(255))
    insaddr_insid = db.Column(db.NVARCHAR(255))
    curr_insid = db.Column(db.NVARCHAR(255))
    quantity = db.Column(db.DECIMAL(18, 4))
    acquirer_ptynbr_ptyid = db.Column(db.NVARCHAR(255))
    counterparty_ptynbr_ptyid = db.Column(db.NVARCHAR(255))
    owner_usrnbr_userid = db.Column(db.NVARCHAR(255))
    prfnbr_prfid = db.Column(db.NVARCHAR(255))
    MessageBuilder = db.Column(db.NVARCHAR)
    ResponseFromAMB = db.Column(db.NVARCHAR)
    CreationTime = db.Column(db.DateTime)
    CreationId = db.Column(db.Integer)
    LastModification = db.Column(db.DateTime)
    LastModifierId = db.Column(db.Integer)
    IsDeleted = db.Column(db.Boolean)
    DeletedId = db.Column(db.Integer)
    DeletionTime = db.Column(db.DateTime)

    @classmethod
    @auth.login_required
    def find_by_id(cls, _id) -> "TradeModel":
        return cls.query.filter_by(Id=_id).first()

    @classmethod
    @auth.login_required
    def find_by_name(cls, name) -> "TradeModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        trade = TradeModel(
            type=self.type,
            time=self.time,
            insaddr_insid=self.insaddr_insid,
            curr_insid=self.curr_insid,
            quantity=self.quantity,
            acquirer_ptynbr_ptyid=self.acquirer_ptynbr_ptyid,
            counterparty_ptynbr_ptyid=self.counterparty_ptynbr_ptyid,
            owner_usrnbr_userid=self.owner_usrnbr_userid,
            prfnbr_prfid=self.prfnbr_prfid,
            MessageBuilder=self.MessageBuilder,
            ResponseFromAMB=self.ResponseFromAMB,
            CreationTime=self.CreationTime,
            CreationId=self.CreationId,
            LastModification=self.LastModification,
            LastModifierId=self.LastModifierId,
            IsDeleted=0,
            DeletedId=None,
            DeletionTime=None
        )
        db.session.add(trade)
        db.session.commit()

    def post_trade_to_fa(self):
        global writer_id
        global check_loop

        amb.mb_enable_unicode()
        amb.mb_init(ambAddress)

        logger.debug('Connected to amb.')

        try:
            writer_id = amb.mb_queue_init_writer(writer_name, message_sent_cb, None)
        except RuntimeError as error:
            logger.error(f'writing message failed. {error}')
        logger.debug(f'Writer_id:... {writer_id}')

        date_now = datetime.datetime.now()

        message = amb.mbf_start_message(None, 'SYNC_INSERT_TRADE', '1.0', str(date_now), writer_name)

        list_mdf = message.mbf_start_list('TRADE')
        list_mdf.mbf_add_string('TYPE', self.type)
        list_mdf.mbf_add_string('TIME', str(self.time))
        list_mdf.mbf_add_string('INSADDR.INSID', self.insaddr_insid)
        list_mdf.mbf_add_string('CURR.INSID', self.curr_insid)
        list_mdf.mbf_add_string('QUANTITY', str(self.quantity))
        list_mdf.mbf_add_string('ACQUIRER_PTYNBR.PTYID', self.acquirer_ptynbr_ptyid)
        list_mdf.mbf_add_string('COUNTERPARTY_PTYNBR.PTYID', self.counterparty_ptynbr_ptyid)
        list_mdf.mbf_add_string('OWNER_USRNBR.USERID', self.owner_usrnbr_userid)
        list_mdf.mbf_add_string('PRFNBR.PRFID', self.prfnbr_prfid)
        list_mdf.mbf_end_list()

        tmp = message.mbf_end_message()
        TradeModel.MessageBuilder = tmp.mbf_object_to_string()
        TradeModel.CreationTime = date_now

        logger.debug(f'Sending:...{tmp.mbf_object_to_string()}')

        message_as_string = message.mbf_object_to_string()
        message_size = sys.getsizeof(message_as_string)
        try:
            ret_val = amb.mb_queue_write_sync(writer_id, trade_subject, message_as_string, message_size, 'OK', reply_cb,
                                              "This is argument...")
            logger.debug(f'retVal = {ret_val}')
        except RuntimeError as error:
            logger.error(f'Message not sent: {error}')

        logger.debug('Message sent')
        logger.debug('Waiting for events...\n')
        count = 0
        logger.debug(f'Value of var before the loop: {check_loop}')
        while check_loop != 1:
            count = count + 1
            amb.mb_poll()
            logger.debug(f'Value of count {count}')

        logger.debug('Sent the message.')
        check_loop = 0
