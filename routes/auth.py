from flask import Blueprint, request, jsonify
from app import db, jwt_blacklist
from models.user import User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    role = data.get('role', 'customer')

    user = User(
        name=data['name'],
        email=data['email'],
        role=role
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(msg="Register success")


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(
            identity=str(user.id),  #
            additional_claims={"role": user.role}
        )

        return jsonify(access_token=token)
    return jsonify(msg="Invalid login"), 401


# LOGOUT
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_blacklist.add(jti)
    return jsonify(msg="Logout success")
