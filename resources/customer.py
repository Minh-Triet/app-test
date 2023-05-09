from flask import request
from flask_restful import Resource
from loguru import logger

from authentication import auth
from models.customer import CustomerModel
from schemas.customer import CustomerSchema

TRADE_ALREADY_EXISTS = "A trade with that id already exists."
CREATED_SUCCESSFULLY = "Trade created successfully."
TRADE_NOT_FOUND = "Trade is not found."
TRADE_DELETED = "Trade is deleted."
ERROR_INSERTING = "An error occurred while inserting the trade."

customer_schema = CustomerSchema()


class Customer(Resource):
    @classmethod
    @auth.login_required
    def post(cls):
        customer_json = request.get_json()
        customer = customer_schema.load(customer_json)

        try:
            customer.post_customer_to_fa()
            customer.save_to_db()
        except RuntimeError as error:
            return {'message': ERROR_INSERTING + f'. Detail: {error}'}, 500

        return {'message': CustomerModel.ResponseFromAMB}, 201


class CustomerList(Resource):
    @classmethod
    def get(cls):
        return {'message': [customer.jsonify() for customer in CustomerModel.query.all()]}


class CustomerDetail(Resource):
    @classmethod
    @auth.login_required
    def get(cls, _id):
        customer = CustomerModel.find_by_id(_id)
        if customer:
            return customer_schema.dump(customer), 200
        return {'message': f'Customer Id {_id} is not not found'}, 404
