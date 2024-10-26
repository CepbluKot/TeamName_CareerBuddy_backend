import pandas as pd
import logging
import datetime
from sqlalchemy import select
from schemas.employees import Roles, Departments
from faker import Faker
from settings import db

from schemas.career_goals import CareerGoals, GoalCheckpoints


f = Faker()

def generate_goals(employee_id: int, goals_amount: int = 10, goals_checkpoints_amount: int = 3):    
    for _ in range(goals_amount):
        career_goal_db_record = CareerGoals(
            employee_id=employee_id,
            name = f.text(30),
            description=f.text(77),
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=365)
        )

        db.session.add(career_goal_db_record)

        try:
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            logging.error(f'error occupied during flushing goals: {e}')

        goal_id = career_goal_db_record.id

        for _ in range(goals_checkpoints_amount):
            career_goal_checkpoint_db_record = GoalCheckpoints(
                career_goal_id=goal_id,
                description = f.text(77),
                start_date=datetime.datetime.now(),
                end_date=datetime.datetime.now() + datetime.timedelta(days=299)
            )
            db.session.add(career_goal_checkpoint_db_record)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'error occupied during generating goals: {e}')
