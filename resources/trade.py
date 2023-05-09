from flask_restful import Resource
from flask import request
from models.trade import TradeModel
from schemas.trade import TradeSchema
from loguru import logger
from authentication import auth

TRADE_ALREADY_EXISTS = "A trade with that id already exists."
CREATED_SUCCESSFULLY = "Trade created successfully."
TRADE_NOT_FOUND = "Trade is not found."
TRADE_DELETED = "Trade is deleted."
ERROR_INSERTING = "An error occurred while inserting the trade."

trade_schema = TradeSchema()


class Trade(Resource):
    @classmethod
    @auth.login_required
    def post(cls):
        trade_json = request.get_json()
        logger.debug(f'trade json: {trade_json}')
        trade_data = trade_schema.load(trade_json)

        try:
            trade_data.post_trade_to_fa()
            trade_data.save_to_db()
        except RuntimeError as error:
            return {'message': ERROR_INSERTING + f' Detail: {error}'}, 500

        return {'message': TradeModel.ResponseFromAMB}, 201


class TradeList(Resource):

    @auth.login_required
    def get(self):
        return {'trades': [trade.json() for trade in TradeModel.query.all()]}


class TradeDetail(Resource):
    @classmethod
    @auth.login_required
    def get(cls, _id):
        trade = TradeModel.find_by_id(_id)
        if trade:
            return trade_schema.dump(trade), 200
        return {'message': f'Trade Id {_id} is not found'}, 404
