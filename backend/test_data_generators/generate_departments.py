import pandas as pd
from schemas.employees import Departments
from settings import db


def generate_departments():
    df = pd.read_csv('dataset.csv')
    all_departments = set(df.loc[:,'Department'])
    all_departments = sorted(all_departments)

    for department in all_departments:
        department_db_record = Departments( name=department )
        
        db.session.add(department_db_record)
    db.session.commit()
