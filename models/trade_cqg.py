# import quickfix
from dateutil import parser
from loguru import logger

from db import db

__SOH__ = chr(1)

from strings.fix_message import getMsgType, getExecTransType, getOrdStatus, getSide, getTimeInForce, getExecType, \
    getCustOrderHandlingInst


class TradeCQG(db.Model):
    __tablename__ = 'TradeCQG'
    IdentityID = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    MessageRaw = db.Column(db.String(100))
    Message = db.Column(db.String(100))
    BeginString = db.Column(db.String(100))
    OnBehalfOfCompID = db.Column(db.String(100))
    BodyLength = db.Column(db.Integer)
    MsgType = db.Column(db.String(100))
    MsgSeqNum = db.Column(db.Integer)
    SenderCompID = db.Column(db.String(32))
    SendingTime = db.Column(db.DateTime)
    TargetCompID = db.Column(db.String(32))
    TargetSubID = db.Column(db.String)
    DeliverToSubID = db.Column(db.String(32))
    TargetLocationID = db.Column(db.String(12))
    Account = db.Column(db.String(32))
    AvgPx = db.Column(db.DECIMAL(18, 8))
    ClOrdID = db.Column(db.String(64))
    CumQty = db.Column(db.DECIMAL(18, 4))
    Currency = db.Column(db.String(32))
    ExecID = db.Column(db.String(100))
    ExecTransType = db.Column(db.String(100))
    IDSource = db.Column(db.String(100))
    LastMkt = db.Column(db.String(4))
    LastPx = db.Column(db.DECIMAL(18, 8))
    OrderID = db.Column(db.String(32))
    OrderQty = db.Column(db.DECIMAL(18, 4))
    OrdStatus = db.Column(db.String(100))
    OrdType = db.Column(db.String(100))
    Price = db.Column(db.DECIMAL(18, 8))
    SecurityID = db.Column(db.String(100))
    Side = db.Column(db.String(100))
    Symbol = db.Column(db.String(64))
    TimeInForce = db.Column(db.String(100))
    TransactTime = db.Column(db.DateTime)
    ExecType = db.Column(db.String(100))
    LeavesQty = db.Column(db.DECIMAL(18, 4))
    SecurityType = db.Column(db.String(100))
    SecondaryOrderID = db.Column(db.String(100))
    MaturityMonthYear = db.Column(db.String(100))
    MaturityDay = db.Column(db.Integer)
    SecurityExchange = db.Column(db.String(100))
    MaturityDate = db.Column(db.DateTime)
    ManualOrderIndicator = db.Column(db.Boolean)
    StatementDate = db.Column(db.DateTime)
    OrderSource = db.Column(db.String(100))
    TradeID = db.Column(db.String(100))
    ChainOrderID = db.Column(db.String(100))
    OrderPlacementTime = db.Column(db.DateTime)
    ExchangeKeyID = db.Column(db.String(10))
    FillExecID = db.Column(db.String(64))
    SendingTimeHR = db.Column(db.DateTime)
    TransactTimeHR = db.Column(db.DateTime)
    MifidExecutionDecision = db.Column(db.String(100))
    MifidExecutionDecisionIsAlgo = db.Column(db.Boolean)
    TodayCutoff = db.Column(db.DateTime)
    ContractDate = db.Column(db.DateTime)
    ContractDay = db.Column(db.Integer)
    ContractMonthYear = db.Column(db.String(100))
    SecondaryClOrderID = db.Column(db.String(100))
    ClearingBusinessDate = db.Column(db.DateTime)
    SecuritySubType = db.Column(db.String(100))
    CustOrderHandlingInst = db.Column(db.String(100))
    CheckSum = db.Column(db.String(100))


def trade_fix(message):
    try:
        BeginString = message.getHeader().getField(8)
        BodyLength = message.getHeader().getField(9)
        MsgType = message.getHeader().getField(35)
        MsgSeqNum = message.getHeader().getField(34)
        SenderCompID = message.getHeader().getField(49)
        SendingTime = message.getHeader().getField(52)
        TargetCompID = message.getHeader().getField(56)
        TargetSubID = message.getHeader().getField(57)
        DeliverToSubID = message.getHeader().getField(129)
        TargetLocationID = message.getHeader().getField(143)
        Account = message.getField(1)
        AvgPx = message.getField(6)
        ClOrdID = message.getField(11)
        CumQty = message.getField(14)
        OnBehalfOfCompID = None
        Currency = None
        LastPx = None
        Price = None
        SecondaryOrderID = None
        StatementDate = None
        TradeID = None
        FillExecID = None
        SecondaryClOrderID = None
        ClearingBusinessDate = None
        TodayCutoff = None
        ExecID = message.getField(17)
        ExecTransType = message.getField(20)
        IDSource = message.getField(22)
        LastMkt = message.getField(30)
        OrderID = message.getField(37)
        OrderQty = message.getField(38)
        OrdStatus = message.getField(39)
        OrdType = message.getField(40)
        SecurityID = message.getField(48)
        Side = message.getField(54)
        Symbol = message.getField(55)
        TimeInForce = message.getField(59)
        TransactTime = message.getField(60)
        ExecType = message.getField(150)
        LeavesQty = message.getField(151)
        SecurityType = message.getField(167)
        MaturityMonthYear = message.getField(200)
        MaturityDay = message.getField(205)
        SecurityExchange = message.getField(207)
        MaturityDate = message.getField(541)
        ManualOrderIndicator = message.getField(1028)
        if ManualOrderIndicator == 'Y':
            ManualOrderIndicator = True
        else:
            ManualOrderIndicator = False
        OrderSource = message.getField(20026)
        ChainOrderID = message.getField(20029)
        OrderPlacementTime = message.getField(20111)
        ExchangeKeyID = message.getField(20119)
        SendingTimeHR = message.getField(20173)
        TransactTimeHR = message.getField(20175)
        MifidExecutionDecision = message.getField(20180)
        MifidExecutionDecisionIsAlgo = message.getField(20182)
        if MifidExecutionDecisionIsAlgo == 'Y':
            MifidExecutionDecisionIsAlgo = True
        else:
            MifidExecutionDecisionIsAlgo = False
        ContractDate = message.getField(20607)
        ContractDay = message.getField(20608)
        ContractMonthYear = message.getField(20609)
        SecuritySubType = message.getField(50762)
        CustOrderHandlingInst = message.getField(51031)
        CheckSum = message.getTrailer().getField(10)
        try:
            OnBehalfOfCompID = message.getField(115)
            ClearingBusinessDate = parser.parse(message.getField(50715))
            Currency = message.getField(15)
            SecondaryClOrderID = message.getField(50526)
            TodayCutoff = parser.parse(message.getField(20193))
            FillExecID = message.getField(20122)
            TradeID = message.getField(20027)
            StatementDate = parser.parse(message.getField(20023))
            LastPx = float(message.getField(31))
            SecondaryOrderID = message.getField(198)
            Price = float(message.getField(44))

        except Exception as e:
            logger.debug(e)
        trade = TradeCQG(
            MessageRaw=message.toString().replace(__SOH__, "|"),
            Message=None,
            BeginString=BeginString,
            BodyLength=int(BodyLength),
            MsgType=getMsgType(MsgType),
            MsgSeqNum=int(MsgSeqNum),
            SenderCompID=SenderCompID,
            SendingTime=parser.parse(SendingTime),
            TargetCompID=TargetCompID,
            TargetSubID=TargetSubID,
            DeliverToSubID=DeliverToSubID,
            TargetLocationID=TargetLocationID,
            Account=Account,
            AvgPx=float(AvgPx),
            ClOrdID=ClOrdID,
            CumQty=float(CumQty),
            Currency=Currency,
            ExecID=ExecID,
            ExecTransType=getExecTransType(ExecTransType),
            IDSource=IDSource,
            LastMkt=LastMkt,
            LastPx=LastPx,
            OrderID=OrderID,
            OrderQty=float(OrderQty),
            OrdStatus=getOrdStatus(OrdStatus),
            OrdType=OrdType,
            Price=Price,
            SecurityID=SecurityID,
            Side=getSide(Side),
            Symbol=Symbol,
            TimeInForce=getTimeInForce(TimeInForce),
            TransactTime=parser.parse(TransactTime),
            ExecType=getExecType(ExecType),
            LeavesQty=float(LeavesQty),
            SecurityType=SecurityType,
            SecondaryOrderID=SecondaryOrderID,
            MaturityMonthYear=MaturityMonthYear,
            MaturityDay=int(MaturityDay),
            SecurityExchange=SecurityExchange,
            MaturityDate=parser.parse(MaturityDate),
            ManualOrderIndicator=ManualOrderIndicator,
            StatementDate=StatementDate,
            OrderSource=OrderSource,
            TradeID=TradeID,
            ChainOrderID=ChainOrderID,
            OrderPlacementTime=parser.parse(OrderPlacementTime),
            ExchangeKeyID=ExchangeKeyID,
            FillExecID=FillExecID,
            SendingTimeHR=parser.parse(SendingTimeHR),
            TransactTimeHR=parser.parse(TransactTimeHR),
            MifidExecutionDecision=MifidExecutionDecision,
            MifidExecutionDecisionIsAlgo=MifidExecutionDecisionIsAlgo,
            TodayCutoff=TodayCutoff,
            ContractDate=parser.parse(ContractDate),
            ContractDay=int(ContractDay),
            ContractMonthYear=ContractMonthYear,
            SecondaryClOrderID=SecondaryClOrderID,
            ClearingBusinessDate=ClearingBusinessDate,
            SecuritySubType=SecuritySubType,
            CustOrderHandlingInst=getCustOrderHandlingInst(CustOrderHandlingInst),
            CheckSum=CheckSum,
            OnBehalfOfCompID=OnBehalfOfCompID
        )
        messageTranslate = f'BeginString:{trade.BeginString}' + '\n' + f'BodyLength:{trade.BodyLength}\n' + f'MsgType:{trade.MsgType}\n' + f'MsgSeqNum:{trade.MsgSeqNum}\n' + \
                           f'SenderCompID:{trade.SenderCompID}\n' + f'SendingTime:{trade.SendingTime}\n' + f'TargetCompID:{trade.TargetCompID}\n' + f'TargetSubID:{trade.TargetSubID}\n' + \
                           f'DeliverToSubID:{trade.DeliverToSubID}\n' + f'TargetLocationID:{trade.TargetLocationID}\n' + f'Account:{trade.Account}\n' + f'AvgPx:{trade.AvgPx}\n' + \
                           f'ClOrdID:{trade.ClOrdID}\n' + f'CumQty:{trade.CumQty}\n' + f'Currency:{trade.Currency}\n' + f'ExecID:{trade.ExecID}\n' + f'ExecTransType:{trade.ExecTransType}\n' + \
                           f'IDSource:{trade.IDSource}\n' + f'LastMkt:{trade.LastMkt}\n' + f'LastPx:{trade.LastPx}\n' + f'OrderID:{trade.OrderID}\n' + f'OrderQty:{trade.OrderQty}\n' + \
                           f'OrdStatus:{trade.OrdStatus}\n' + f'OrdType:{trade.OrdType}\n' + f'Price:{trade.Price}\n' + f'SecurityID:{trade.SecurityID}\n' + f'Side:{trade.Side}\n' + \
                           f'Symbol:{trade.Symbol}\n' + f'TimeInForce:{trade.TimeInForce}\n' + f'TransactTime:{trade.TransactTime}\n' + f'ExecType:{trade.ExecType}\n' + f'LeavesQty:{trade.LeavesQty}\n' + \
                           f'SecurityType:{trade.SecurityType}\n' + f'SecondaryOrderID:{trade.SecondaryOrderID}\n' + f'MaturityMonthYear:{trade.MaturityMonthYear}\n' + f'MaturityDay:{trade.MaturityDay}\n' + \
                           f'SecurityExchange:{trade.SecurityExchange}\n' + f'MaturityDate:{trade.MaturityDate}\n' + f'ManualOrderIndicator:{trade.ManualOrderIndicator}\n' + f'StatementDate:{trade.StatementDate}\n' + \
                           f'OrderSource:{trade.OrderSource}\n' + f'TradeID:{trade.TradeID}\n' + f'ChainOrderID:{trade.ChainOrderID}\n' + f'OrderPlacementTime:{trade.OrderPlacementTime}\n' + \
                           f'ExchangeKeyID:{trade.ExchangeKeyID}\n' + f'FillExecID:{trade.FillExecID}\n' + f'SendingTimeHR:{trade.SendingTimeHR}\n' + f'TransactTimeHR:{trade.TransactTimeHR}\n' + \
                           f'MifidExecutionDecision:{trade.MifidExecutionDecision}\n' + f'MifidExecutionDecisionIsAlgo:{trade.MifidExecutionDecisionIsAlgo}\n' + f'TodayCutoff:{trade.TodayCutoff}\n' + \
                           f'ContractDate:{trade.ContractDate}\n' + f'ContractDay:{trade.ContractDay}\n' + f'ContractMonthYear:{trade.ContractMonthYear}\n' + f'SecondaryClOrderID:{trade.SecondaryClOrderID}\n' + \
                           f'ClearingBusinessDate:{trade.ClearingBusinessDate}\n' + f'SecuritySubType:{trade.SecuritySubType}\n' + f'CustOrderHandlingInst:{trade.CustOrderHandlingInst}\n' + f'CheckSum:{trade.CheckSum}\n' + f'OnBehalfOfCompID:{trade.OnBehalfOfCompID}'
        trade.Message = messageTranslate
        db.session.add(trade)
        db.session.commit()
    except Exception as e:
        logger.debug(e)


