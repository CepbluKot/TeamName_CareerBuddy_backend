import datetime
from faker import Faker
from jinja2 import Environment, FileSystemLoader, select_autoescape
from random import randint


fake = Faker()

current_date = datetime.datetime.now()
future_date = current_date + datetime.timedelta(days=365)

data = {
    "workload_answer": fake.text(max_nb_chars=123),  
    "work_life_balance_answer": randint(1,4),  
}

jinja_env = Environment(
    loader=FileSystemLoader("."), 
    autoescape=select_autoescape(['html', 'xml', 'json']) 
)

template = jinja_env.get_template('rofl.json.j2')

body = template.render(**data)

print(body)
