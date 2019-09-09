"""Expense views"""
from flask import Blueprint, request, jsonify
from expense_tracker.utils import requires_auth, retrieve_auth_token
from flask.views import MethodView
from expense_tracker.user.models import User
from .models import Expense, Period
from .schema import expense_schema, period_schema

blueprint = Blueprint("expense", __name__, url_prefix="/expense", static_folder="../static")


class PeriodAPI(MethodView):
    decorators = (requires_auth, )

    def get(self, record_id):
        auth_token = retrieve_auth_token(request)
        user = User.get_by_auth_token(auth_token)

        if user:
            if not record_id:
                periods = Period.get_all_by_user_id(user.id)
                if not periods:
                    return jsonify(dict())
                return period_schema.dump(periods, many=True)
            return period_schema.dump(Period.query.filter(user_id=user.id, id=record_id))


period_view = PeriodAPI.as_view('period_api')
blueprint.add_url_rule('/', defaults={'record_id': None}, view_func=period_view, methods=['GET', ])
blueprint.add_url_rule('/', view_func=period_view, methods=['POST', ])
blueprint.add_url_rule('/<int:record_id>', view_func=period_view, methods=['GET', 'PATCH', 'DELETE'])


# class ExpenseAPI(MethodView):
#     decorators = (requires_auth, )
#
#     def get(self, record_id):
#         if not record_id:
#             users = User.query.all()
#             if not users:
#                 return jsonify(dict())
#             return user_schema.dump(User.query.all(), many=True)
#         return user_schema.dump(User.get_by_id(user_id))

