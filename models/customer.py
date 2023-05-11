import logging
import sys
import datetime
# import amb
from loguru import logger
from constants.amb_server import ambAddress, writer_name, party_subject
from db import db

writer_id = 0
reader_id = 0
check_loop = 0


def reply_cb(message, status, arg):
    logger.debug('Reply from AMB server:...')
    buf = amb.mbf_create_buffer_from_data(message.data_p)
    message_from_amb = buf.mbf_read()

    date_now = datetime.datetime.now()
    CustomerModel.LastModification = date_now
    CustomerModel.ResponseFromAMB = message_from_amb.mbf_object_to_string_xml()
    logger.debug(message_from_amb.mbf_object_to_string_xml())
    global check_loop

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
        logger.debug('Disconnected ...')

    elif event_string == 'Async':
        logger.debug("Async")


# Create table CustomerTransaction
class CustomerModel(db.Model):
    __tablename__ = 'CustomerTransaction'
    Id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.String(1000))
    SwiftCode = db.Column(db.String(50))
    Name = db.Column(db.String)
    FullName = db.Column(db.String)
    AdditionalFullName = db.Column(db.String)
    Address = db.Column(db.String)
    AdditionalAddress = db.Column(db.String)
    City = db.Column(db.String)
    Country = db.Column(db.String(255))
    BISStatus = db.Column(db.String(255))
    BusinessStatus = db.Column(db.String(255))
    Parent = db.Column(db.String(255))
    MessageBuilder = db.Column(db.String)
    ResponseFromAMB = db.Column(db.String)
    CreationTime = db.Column(db.DateTime)
    CreationId = db.Column(db.Integer)
    LastModification = db.Column(db.DateTime)
    LastModifierId = db.Column(db.Integer)
    IsDeleted = db.Column(db.Boolean)
    DeletedId = db.Column(db.Integer)
    DeletionTime = db.Column(db.DateTime)

    @classmethod
    def find_by_id(cls, _id) -> "CustomerModel":
        return cls.query.filter_by(Id=_id).first()

    @classmethod
    def find_by_name(cls, name) -> "CustomerModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        customer = CustomerModel(
            CustomerID=self.CustomerID,
            SwiftCode=self.SwiftCode,
            Name=self.Name,
            FullName=self.FullName,
            AdditionalFullName=self.AdditionalFullName,
            Address=self.Address,
            AdditionalAddress=self.AdditionalAddress,
            City=self.City,
            Country=self.Country,
            BISStatus=self.BISStatus,
            BusinessStatus=self.BusinessStatus,
            Parent=self.Parent,
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
        db.session.add(customer)
        db.session.commit()

    def post_customer_to_fa(self):
        global writer_id
        global check_loop

        amb.mb_enable_unicode()
        amb.mb_init(ambAddress)

        logger.debug('Connected to AMB at customer model.')

        writer_id = amb.mb_queue_init_writer(writer_name, message_sent_cb, None)

        date_now = datetime.datetime.now()
        message = amb.mbf_start_message(None, 'SYNC_INSERT_PARTY', '1.0', str(date_now), writer_name)

        list_customer = message.mbf_start_list('PARTY')
        list_customer.mbf_add_string('PTYID', self.CustomerID)
        list_customer.mbf_add_string('PTYID2', self.Name)
        list_customer.mbf_add_string('FULLNAME', self.FullName)
        list_customer.mbf_add_string('FULLNAME2', self.AdditionalFullName)
        list_customer.mbf_add_string('SWIFT', self.SwiftCode)
        list_customer.mbf_add_string('CITY', self.City)
        list_customer.mbf_add_string('COUNTRY', self.Country)
        list_customer.mbf_add_string('BIS_STATUS', self.BISStatus)
        list_customer.mbf_add_string('BUSINESS_STATUS_CHLNBR.ENTRY', self.BusinessStatus)
        list_customer.mbf_add_string('BUSINESS_STATUS_CHLNBR.LIST', 'Business Status')
        list_customer.mbf_add_string('PARENT_PTYNBR', self.Parent)
        list_customer.mbf_add_string('ADDRESS', self.Address)
        list_customer.mbf_add_string('ADDRESS2', self.AdditionalAddress)

        list_customer.mbf_end_list()

        tmp = message.mbf_end_message()
        CustomerModel.MessageBuilder = tmp.mbf_object_to_string()
        CustomerModel.CreationTime = date_now

        message_as_string = message.mbf_object_to_string()
        message_size = sys.getsizeof(message_as_string)
        try:
            ret_val = amb.mb_queue_write_sync(writer_id, party_subject, message_as_string, message_size, 'OK', reply_cb,
                                              "This is argument...")
            logger.debug(f'retVal = {ret_val}')
        except RuntimeError as error:
            logger.error(f'Message not sent: {error}')

        logger.debug('Message sent')
        logger.debug('Waiting for events...\n')
        count = 0

        while check_loop != 1:
            count = count + 1
            amb.mb_poll()
            logger.debug(f'Value of var inside the loop: {check_loop}')

        logger.debug('Sent the message.')
        check_loop = 0
