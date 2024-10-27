import threading
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from settings import app, db, admin
from routes.employees import api as employees_api
from routes.auth import api as auth_api
from routes.feedback import api as feedback_api
from routes.career_goals import api as career_goals_api
from routes.departments import api as departments_api
from routes.roles import api as roles_api

from test_data_generators.generate_all import generate_test_data

from schemas.career_goals import CareerGoals, GoalCheckpoints
from schemas.feedback import Feedback, FeedbackTemplates
from schemas.employees_auth import EmployeesAuth
from schemas.employees import Employees, Roles, Departments


migrate = Migrate(app, db)
app.register_api(employees_api)
app.register_api(auth_api)
app.register_api(feedback_api)
app.register_api(career_goals_api)
app.register_api(departments_api)
app.register_api(roles_api)


admin.add_view(ModelView(CareerGoals, db.session))
admin.add_view(ModelView(GoalCheckpoints, db.session))
admin.add_view(ModelView(Feedback, db.session))
admin.add_view(ModelView(FeedbackTemplates, db.session))
admin.add_view(ModelView(EmployeesAuth, db.session))
admin.add_view(ModelView(Employees, db.session))
admin.add_view(ModelView(Roles, db.session))
admin.add_view(ModelView(Departments, db.session))


if __name__ == "__main__":
    data_generator_thr = threading.Thread(target=generate_test_data)
    data_generator_thr.daemon = True
    data_generator_thr.start()

    app.run(debug=False, port=8000, host="0.0.0.0")

    generate_test_data()
