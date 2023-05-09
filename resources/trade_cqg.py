import logging

from flask import render_template, make_response, request
from flask_restful import Resource
# import quickfix
from flask_wtf import FlaskForm
from loguru import logger
from wtforms import StringField
from wtforms.validators import DataRequired

from authentication import auth
# import quickfix as fix

__SOH__ = chr(1)

from db import db

from models.trade_cqg import trade_fix

isStart = False
isStop = False


class TradeCQG(Resource):
    @classmethod
    # @auth.login_required()
    def post(cls):
        global isStart, initiator, isStop, status
        if request.form.get('Start') == 'Start':
            try:
                if isStart is False and isStop is False:
                    # settings = quickfix.SessionSettings('client.cfg')
                    # application = Application()
                    # storeFactory = quickfix.FileStoreFactory(settings)
                    # logFactory = quickfix.FileLogFactory(settings)
                    # initiator = quickfix.SocketInitiator(application, storeFactory, settings, logFactory)
                    # initiator.start()

                    isStart = True
                    status = 'Started'

                if isStop is True and isStart is True:
                    initiator.start()
                    isStop = False
                    status = 'Started'
            except Exception as e:
                logger.debug(f'ERROR: {e}')
                initiator.stop()
                status = 'Stopped'
        elif request.form.get('Stop') == 'Stop':
            initiator.stop()
            isStop = True
            status = 'Stopped'

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('cqg_trade.html', status=status), 200, headers)

    @classmethod
    # @auth.login_required()
    def get(cls):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('cqg_trade.html'), 200, headers)


# class Application(fix.Application):
#     """FIX Application"""
#
#     def __init__(self):
#         super().__init__()
#         self.sessionID = None
#
#     def onCreate(self, sessionID):
#         logger.debug("onCreate : Session (%s)" % sessionID.toString())
#         return
#
#     def onLogon(self, sessionID):
#         self.sessionID = sessionID
#         logger.debug("Successful Logon to session '%s'." % sessionID.toString())
#         return
#
#     def onLogout(self, sessionID):
#         logger.debug("Session (%s) logout !" % sessionID.toString())
#         return
#
#     def toAdmin(self, message, sessionID):
#         msgType = fix.MsgType()
#         message.getHeader().getField(msgType)
#         msg = message.toString().replace(__SOH__, "|")
#         if msgType.getValue() == fix.MsgType_Logon:
#             message.setField(fix.SenderSubID("TestFIXSessionPersist"))
#             message.setField(fix.RawData("pass"))
#         if msgType.getValue() == fix.MsgType_Reject:
#             logger.debug(f'(Admin) Reject: {msg}')
#         else:
#             logger.debug(f'(Admin) Sending: {msg}')
#
#         return
#
#     def fromAdmin(self, message, sessionID):
#         msg = message.toString().replace(__SOH__, "|")
#         logger.debug(f'(Admin) Receive: {msg}')
#         return
#
#     def toApp(self, message, sessionID):
#         msg = message.toString().replace(__SOH__, "|")
#         logger.debug(f'(App) Sending: {msg}')
#         return
#
#     def fromApp(self, message, sessionID):
#         ExecType = fix.ExecType()
#         message.getField(ExecType)
#         msg = message.toString().replace(__SOH__, "|")
#         if ExecType.getValue() == fix.ExecType_FILL:
#             logger.debug(f'(App) Receive Execution Report: {msg}')
#             try:
#                 from app import app
#                 with app.app_context():
#                     db.init_app(app)
#                     trade_fix(message)
#             except Exception as e:
#                 logging.debug(e)
#             # or ExecType.getValue() == fix.ExecType_CANCELED
#             # logger.debug(f'(App) Receive: {msg}')
#         return
