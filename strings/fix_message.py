def getMsgType(MsgType):
    if MsgType == '3':
        MsgType = 'Reject'
    if MsgType == '8':
        MsgType = 'Execution Report'
    if MsgType == 'F':
        MsgType = 'Order Cancel Request'

    return MsgType


def getExecTransType(ExecTransType):
    if ExecTransType == '0':
        ExecTransType = 'New'
    if ExecTransType == '1':
        ExecTransType = 'Cancel'
    if ExecTransType == '2':
        ExecTransType = 'Correct'
    if ExecTransType == '3':
        ExecTransType = 'Status [response to Order Mass Status Request (UAF)]'

    return ExecTransType


def getOrdStatus(OrdStatus):
    if OrdStatus == '0':
        OrdStatus = 'New'
    if OrdStatus == '1':
        OrdStatus = 'Partially filled'
    if OrdStatus == '2':
        OrdStatus = 'Filled'
    if OrdStatus == '4':
        OrdStatus = 'Canceled'
    if OrdStatus == '5':
        OrdStatus = 'Replaced'
    if OrdStatus == '6':
        OrdStatus = 'Pending Cancel'
    if OrdStatus == '8':
        OrdStatus = 'Rejected'
    if OrdStatus == '9':
        OrdStatus = 'Suspended'
    if OrdStatus == 'A':
        OrdStatus = 'Pending New'
    if OrdStatus == 'C':
        OrdStatus = 'Expired'
    if OrdStatus == 'E':
        OrdStatus = 'Pending Replace'

    return OrdStatus


def getSide(Side):
    if Side == '1':
        Side = 'Buy'
    if Side == '2':
        Side = 'Sell'
    if Side == '3':
        Side = 'Buy minus'
    if Side == '4':
        Side = 'Sell plus'
    if Side == '5':
        Side = 'Sell short'
    if Side == '6':
        Side = 'Sell short exempt'
    if Side == '7':
        Side = 'Undisclosed'
    if Side == '8':
        Side = 'Cross'
    if Side == '9':
        Side = 'Cross short'

    return Side


def getTimeInForce(TimeInForce):
    if TimeInForce == '0':
        TimeInForce = 'DAY'
    if TimeInForce == '1':
        TimeInForce = 'Good Till Cancel (GTC)'
    if TimeInForce == '3':
        TimeInForce = 'Immediate or Cancel (IOC)'
    if TimeInForce == '4':
        TimeInForce = 'Fill or Kill (FOK)'
    if TimeInForce == '6':
        TimeInForce = 'Good Till Date (GTD)'
    if TimeInForce == '5':
        TimeInForce = 'Good Till Crossing (GTX)'

    return TimeInForce


def getExecType(ExecType):
    if ExecType == '0':
        ExecType = 'New'
    if ExecType == '1':
        ExecType = 'Partially filled'
    if ExecType == '2':
        ExecType = 'Filled'
    if ExecType == '4':
        ExecType = 'Canceled'
    if ExecType == '5':
        ExecType = 'Replaced'
    if ExecType == '6':
        ExecType = 'Pending Cancel'
    if ExecType == '8':
        ExecType = 'Rejected'
    if ExecType == '9':
        ExecType = 'Suspended'
    if ExecType == 'A':
        ExecType = 'Pending New'
    if ExecType == 'C':
        ExecType = 'Expired'
    if ExecType == 'E':
        ExecType = 'Pending Replace'

    return ExecType


def getCustOrderHandlingInst(CustOrderHandlingInst):
    if CustOrderHandlingInst == 'W':
        CustOrderHandlingInst = 'Desk'
    if CustOrderHandlingInst == 'Y':
        CustOrderHandlingInst = 'Electronic'
    if CustOrderHandlingInst == 'C':
        CustOrderHandlingInst = 'Vendor-provided Platform billed by Executing Broker'
    if CustOrderHandlingInst == 'G':
        CustOrderHandlingInst = 'Sponsored Access via Exchange API or FIX provided by Executing Broker'
    if CustOrderHandlingInst == 'H':
        CustOrderHandlingInst = 'Premium Algorithmic Trading Provider billed by Executing Broker'
    if CustOrderHandlingInst == 'D':
        CustOrderHandlingInst = 'Other, including Other-provided Screen'

    return CustOrderHandlingInst
