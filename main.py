import os
from flask import Flask, render_template
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig, TestingConfig, Production
from application.data.database import db
from flask_jwt_extended import JWTManager

app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")

    # if os.getenv('ENV', "development") == "development":
    #     app.config.from_object(LocalDevelopmentConfig)
    # elif os.getenv('ENV', "development") == 'testing':
    #     app.config.from_object(TestingConfig)
    app.config.from_object(Production)

    db.init_app(app)
    app.app_context().push()

    api = Api(app)
    app.app_context().push()

    jwt = JWTManager(app)
    app.app_context().push()

    return app, api, jwt

app, api, jwt = create_app()

from application.controller.api import *

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404

@app.errorhandler(403)
def not_authorized(e):
    return "Not Authorized", 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)