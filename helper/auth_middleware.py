from flask_jwt_extended import get_jwt_identity, get_jwt
from functools import wraps
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims or claims.get('role') != 'admin':
            return jsonify(msg="Admin only"), 403
        return fn(*args, **kwargs)
    return wrapper


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if not identity:
            return jsonify(msg="Login required"), 401
        return fn(*args, **kwargs)
    return wrapper

