from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from settings import app, db
# import backend.routes.employees
from routes.employees import api as employees_api


migrate = Migrate(app, db)
# app.register_blueprint(routes.employees.bp)
app.register_api(employees_api)
# app.register_api(test_api)


if __name__ == '__main__':
    print('running')
    app.run(debug=False, port=5005, host='0.0.0.0')
