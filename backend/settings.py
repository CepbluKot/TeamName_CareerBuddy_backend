import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_admin import Admin
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_jwt_extended import JWTManager
from sqlalchemy import create_engine

from utils import setting_statsd, StatsdMiddleware


UPLOAD_FOLDER = "./files"

jwt = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}


security_schemes = {"jwt": jwt}

security = [{"jwt": []}]

info = Info(title="CareerBuddy API", version="1.0.0")
app = OpenAPI(__name__, info=info, security_schemes=security_schemes)
cors = CORS(app)
admin = Admin(app, name="CareerBuddy")

app.config["CORS_HEADERS"] = "Content-Type"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:admin@postgres-backend:5432/project"
)

app.config["SECRET_KEY"] = "rofl"
app.config["JWT_SECRET_KEY"] = "prikol"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]


setting_statsd()
app.wsgi_app = StatsdMiddleware(app.wsgi_app, "flask-monitoring")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
db = SQLAlchemy(app)
jwt = JWTManager(app)
token_live_time = datetime.timedelta(hours=3)

engine = create_engine(
    "postgresql+psycopg2://postgres:admin@postgres-backend:5432/project"
)
