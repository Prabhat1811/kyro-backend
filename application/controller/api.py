from flask_restful import fields, reqparse, marshal
from application.utils.validation import *
from application.data.database import db
from application.data.models import *
import bcrypt
from flask import request, jsonify
from main import app, jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid
from flask_cors import cross_origin


@app.route('/api/user/register', methods=['POST'])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email is None or email == "":
        return jsonify({"msg": "Email is required"}), 401

    if len(password) < 8:
        return jsonify({"msg": "Password should be at least 8 characters long"}), 401

    user = db.session.query(User).filter(User.email == email).first()
    if user:
        return jsonify({"msg": "A User with this email id already exists"}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(id=str(uuid.uuid4()), email=email, password=hashed)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route("/api/user/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = db.session.query(User).filter(User.email == email).first()
    if not user:
        return jsonify({"msg": "Bad email or password"}), 401

    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Bad email or password"}), 401




output_fields_userAPI = {
    "email": fields.String
}

@app.route("/api/user", methods=["GET"])
@jwt_required()
def get_user_email():

    user_id = get_jwt_identity()

    user = db.session.query(User).filter(User.id == user_id).first()

    try:
        return marshal(user, output_fields_userAPI)
    except:
        return jsonify({}), 404




output_fields_LikedShowsAPI = {
    "show_id": fields.Integer,
}

@app.route("/api/liked_shows", methods=["GET"])
@jwt_required()
def get_liked_shows():
    user_id = get_jwt_identity()
    
    liked_shows = db.session.query(LikedShows).filter(LikedShows.user_id == user_id).all()

    if liked_shows is None:
        return {}

    try:
        return marshal(liked_shows, output_fields_LikedShowsAPI)
    except:
        jsonify({}), 404


create_LikedShows_parser = reqparse.RequestParser()
create_LikedShows_parser.add_argument("show_id")

@app.route("/api/liked_shows", methods=["POST"])
@jwt_required()
def like_show():
    user_id = get_jwt_identity()

    args = create_LikedShows_parser.parse_args()

    show_id = args.get("show_id", None)

    if show_id is None or show_id == "":
        jsonify({"msg": "Show id is required"}), 400

    liked_show = db.session.query(LikedShows).filter(LikedShows.show_id == show_id and LikedShows.user_id == user_id).first()

    if liked_show is not None:
        db.session.delete(liked_show)
        db.session.commit()
        return jsonify({"msg": "Liked show deleted"}), 201

    else:
        new_liked_show = LikedShows(user_id=user_id, show_id=show_id)
        db.session.add(new_liked_show)
        db.session.commit()

        return jsonify({"msg": "New liked show created"}), 201




output_fields_HistoryAPI = {
    "show_id": fields.Integer
}

@app.route("/api/history", methods=["GET"])
@jwt_required()
def get():

    user_id = get_jwt_identity()

    history = db.session.query(History).filter(History.user_id == user_id).all()

    if history is None:
        return {}

    try:
        return marshal(history, output_fields_HistoryAPI)
    except:
        return  jsonify({}), 404


create_history_parser = reqparse.RequestParser()
create_history_parser.add_argument("show_id")

@app.route("/api/history", methods=["POST"])
@jwt_required()
def post():

    user_id = get_jwt_identity()

    args = create_history_parser.parse_args()

    show_id = args.get("show_id", None)

    if show_id is None or show_id == "":
        return jsonify({"msg": "show_id is required"}), 400

    history = db.session.query(History).filter(History.show_id == show_id and History.user_id == user_id).first()
    if history is not None:
        return jsonify({"msg": "Show already exists"}), 400

    new_history = History(user_id=user_id, show_id=show_id)
    db.session.add(new_history)
    db.session.commit()

    return jsonify({"msg": "Show added to history"}), 201


@app.route("/api/history", methods=["DELETE"])
@jwt_required()
def delete():

    user_id = get_jwt_identity()
    
    history = db.session.query(History).filter(History.user_id == user_id).all()

    for show in history:
        db.session.delete(show)
    db.session.commit()

    return jsonify({"msg": "History deleted"}), 200
