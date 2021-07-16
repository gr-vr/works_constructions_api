from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api()
ma = Marshmallow()