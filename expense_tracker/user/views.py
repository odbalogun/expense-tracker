# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from marshmallow.exceptions import ValidationError
from expense_tracker.extensions import db, csrf_protect
from .schema import user_schema
from .models import User
from sqlalchemy.exc import SQLAlchemyError

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


class UserAPI(MethodView):
    decorators = (csrf_protect.exempt, )

    def get(self, user_id=None):
        if not user_id:
            users = User.query.all()
            if not users:
                return jsonify(dict())
            return user_schema.dump(users, many=True)
        return user_schema.dump(User.get_by_id(user_id))

    def post(self):
        data = request.get_json(force=True)
        try:
            user = user_schema.load(data=data, session=db.session)
            user.save()
            return jsonify({'msg': "Successfully created user"}), 201
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    def patch(self, user_id):
        user = User.get_by_id(user_id)
        data = request.get_json(force=True)
        # remove password & email if included
        data.pop('password', None)
        data.pop('email', None)

        if user:
            try:
                updated_user = user_schema.load(data=data, instance=user)
                updated_user.save()
                return jsonify({'msg': "Successfully updated user"}), 200
            except ValidationError as e:
                return jsonify({'error': e.messages}), 400
            except SQLAlchemyError as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400
        return jsonify({'error': "User not found"}), 404

    def delete(self, user_id):
        user = User.get_by_id(user_id)
        if user:
            user.delete()
            return jsonify({'msg': "Successfully deleted user"}), 200
        return jsonify({'error': "User not found"}), 404


class AuthAPI(MethodView):
    """
    User Login Resource
    """
    # def get(self):
    #     # get the auth token
    #     auth_header = request.headers.get('Authorization')
    #     if auth_header:
    #         try:
    #             auth_token = auth_header.split(" ")[1]
    #         except IndexError:
    #             return jsonify({'error': 'Bearer token malformed.'}), 401
    #     else:
    #         auth_token = ''
    #     if auth_token:
    #         resp = User.decode_auth_token(auth_token)
    #         if not isinstance(resp, str):
    #             return user_schema.dump(User.get_by_id(resp))
    #         return jsonify({'error': resp}), 401
    #     else:
    #         return jsonify({'error': "Provide a valid auth token."}), 401

    def post(self):
        # get the post data
        data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    return jsonify({'msg': "Successfully logged in", 'auth_token': auth_token}), 200
            else:
                return jsonify({'error': "User not found"}), 404
        except Exception as e:
            print(e)
            return jsonify({'error': "Something went wrong. Try again"}), 500


user_view = UserAPI.as_view('user_api')
blueprint.add_url_rule('/', defaults={'user_id': None}, view_func=user_view, methods=['GET', ])
blueprint.add_url_rule('/', view_func=user_view, methods=['POST', ])
blueprint.add_url_rule('/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
blueprint.add_url_rule('/auth/login', view_func=AuthAPI.as_view('auth_api'), methods=['POST'])
# blueprint.add_url_rule('/auth/', view_func=AuthAPI.as_view('auth_api'), methods=['GET'])
