import threading
from flask_migrate import Migrate
from settings import app, db
from routes.employees import api as employees_api
from routes.auth import api as auth_api
from routes.test import api as test_api

from test_data_generators.generate_all import generate_test_data

import schemas.career_goals
import schemas.feedback
import schemas.employees_auth


migrate = Migrate(app, db)
app.register_api(employees_api)
app.register_api(auth_api)
app.register_api(test_api)


if __name__ == '__main__':
    data_generator_thr = threading.Thread(target=generate_test_data)
    data_generator_thr.daemon = True
    data_generator_thr.start()

    app.run(debug=False, port=8000, host='0.0.0.0')

    generate_test_data()
