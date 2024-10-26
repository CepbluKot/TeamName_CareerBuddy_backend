import logging
import pandas as pd
from schemas.employees import Roles
from settings import db


def generate_roles():
    df = pd.read_csv('dataset.csv')
    all_roles = set(df.loc[:,'JobRole'])
    all_roles = sorted(all_roles)

    for role in all_roles:
        role_db_record = Roles( name=role, admin_page=False, feedback_page=True, career_goal_page=True)
        
        if role == 'Human Resources':
            role_db_record = Roles( name=role, admin_page=True, feedback_page=True, career_goal_page=True)
        
        db.session.add(role_db_record)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'error occupied during generating roles: {e}')
