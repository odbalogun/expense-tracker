# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash, request, jsonify
from functools import wraps
from expense_tracker.user.models import User


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


def requires_auth(f):
    """
    Decorator to ensure that client is authenticated
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            return jsonify({'error': 'Please provide your credentials'}), 401

        try:
            token = auth.split(" ")
        except IndexError:
            return jsonify({'error': 'Bearer token malformed.'}), 401

        if token[0] != 'Bearer':
            return jsonify({'error': 'Bad request'}), 500

        if not User.decode_auth_token(token[1]):
            return jsonify({'error': 'Invalid authentication credentials'}), 401
        return f(*args, **kwargs)
    return decorated


def retrieve_auth_token(request_object):
    auth_header = request_object.headers.get('Authorization')

    if auth_header:
        try:
            return auth_header.split(" ")[1]
        except IndexError:
            return -1
    else:
        return -2

