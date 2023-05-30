import time

import quickfix
import quickfix as fix
from loguru import logger

__SOH__ = chr(1)


class Application(fix.Application):
    """FIX Application"""

    def __init__(self):
        super().__init__()
        self.sessionID = None

    def onCreate(self, sessionID):
        logger.debug("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        logger.debug("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        logger.debug("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        msg = message.toString().replace(__SOH__, "|")
        if msgType.getValue() == fix.MsgType_Logon:
            message.setField(fix.SenderSubID("TestFIXSessionPersist"))
            message.setField(fix.RawData("pass"))
        if msgType.getValue() == fix.MsgType_Reject:
            logger.debug(f'(Admin) Reject: {msg}')
        else:
            logger.debug(f'(Admin) Sending: {msg}')

        return

    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logger.debug(f'(Admin) Receive: {msg}')
        return

    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logger.debug(f'(App) Sending: {msg}')
        return

    def fromApp(self, message, sessionID):
        ExecType = fix.ExecType()
        message.getField(ExecType)
        msg = message.toString().replace(__SOH__, "|")
        # if ExecType.getValue() == fix.ExecType_FILL or ExecType.getValue() == fix.ExecType_ORDER_STATUS:
        logger.debug(f'(App) Receive Execution Report: {msg}')

        return


settings = quickfix.SessionSettings("client.cfg")
application = Application()
storeFactory = quickfix.FileStoreFactory(settings)
logFactory = quickfix.FileLogFactory(settings)
initiator = quickfix.SocketInitiator(application, storeFactory, settings, logFactory)
initiator.start()
while True:
    time.sleep(10)
