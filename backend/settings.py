from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI


UPLOAD_FOLDER = './files'

info = Info(title="book API", version="1.0.0")
app = OpenAPI(__name__, info=info)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@postgres-backend:5432/project'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
