import pandas as pd
import logging
from sqlalchemy import select
from schemas.employees import Roles, Departments
from faker import Faker
from settings import db

from schemas.employees import Employees as employees_schema

f = Faker()

def generate_employees():
    df = pd.read_csv('dataset.csv')
    for index, row in df.iterrows():
        job_role =  row["JobRole"]
        department =  row["Department"]
        role_id = db.session.execute(select(Roles.id).where(Roles.name == job_role)).scalars().first()
        department_id = db.session.execute(select(Departments.id).where(Departments.name == department)).scalars().first()
        row = row.to_dict()
        
        name_data = f.name().split(' ')
        name = name_data[0]
        surname = name_data[1]

        employee_db_record = employees_schema(
            name = name,
            surname = surname,
            email = f.email(),
            department_id = department_id,
            role_id = role_id,
            experience = row["TotalWorkingYears"],
            age = row["Age"],
            business_travel = row["BusinessTravel"],
            daily_rate = row["DailyRate"],
            distance_from_home = row["DistanceFromHome"],
            education = row["Education"],
            education_field = row["EducationField"],
            employee_number = row["EmployeeNumber"],
            relationship_satisfaction = row["EnvironmentSatisfaction"],
            standard_hours = row["StandardHours"],
            stock_option_level = row["StockOptionLevel"],
            total_working_years = row["TotalWorkingYears"],
            training_time_last_year = row["TrainingTimesLastYear"],
            work_life_balance = row["WorkLifeBalance"],
            years_at_company = row["YearsAtCompany"],
            years_in_current_role = row["YearsInCurrentRole"],
            years_since_last_promotion = row["YearsSinceLastPromotion"],
            years_with_cur_manager = row["YearsWithCurrManager"]
        )

        db.session.add(employee_db_record)
    
    db.session.commit()
