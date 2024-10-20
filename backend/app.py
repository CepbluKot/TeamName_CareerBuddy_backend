import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from settings import app, db
# import backend.routes.employees
from routes.employees import api as employees_api
from routes.test import api as test_api


migrate = Migrate(app, db)
app.register_api(employees_api)
app.register_api(test_api)


if __name__ == '__main__':
    app.run(debug=False, port=8000, host='0.0.0.0')
