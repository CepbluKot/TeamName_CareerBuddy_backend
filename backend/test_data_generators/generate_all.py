from settings import app
from test_data_generators.generate_departments import generate as generate_departments


def generate_test_data():
    with app.app_context():
        generate_departments(10)
        pass
