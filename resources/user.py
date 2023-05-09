from flask_restful import Resource
from flask import request
# from werkzeug.security import safe_str_cmp
# from flask_jwt_extended import (
#     create_access_token,
#     create_refresh_token
# )
from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": 'Failed to user'}, 400

        user.save_to_db()

        return {"message": 'Done'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": 'Not found'}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": 'Not found'}, 404

        user.delete_from_db()
        return {"message": 'Deleted'}, 200


# class UserLogin(Resource):
#     @classmethod
#     def post(cls):
#         user_json = request.get_json()
#         user_data = user_schema.load(user_json)
#
#         user = UserModel.find_by_username(user_data.username)
#
#         if user and safe_str_cmp(user.password, user_data.password):
#             access_token = create_access_token(identity=user.id, fresh=True)
#             refresh_token = create_refresh_token(user.id)
#             return {"access_token": access_token, "refresh_token": refresh_token}, 200
#
#         return {"message": 'Invalid.'}, 401
