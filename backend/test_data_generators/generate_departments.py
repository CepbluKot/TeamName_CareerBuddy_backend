import random
from schemas.employees import Departments
from settings import db


# List of all possible department names at a tech company
tech_company_departments = [
    # Core Technology Departments
    "Software Development", "Product Development", "Engineering", "Data Science", 
    "Machine Learning/Artificial Intelligence (AI)", "Data Engineering", "Cybersecurity", 
    "Quality Assurance (QA)", "DevOps", "Site Reliability Engineering (SRE)", 
    "Cloud Infrastructure", "Backend Development", "Frontend Development", 
    "Mobile Development", "Full Stack Development", "IT Operations", 
    "Technical Support", "Network Engineering", "Database Administration", 
    "System Architecture", "IT Security", "Embedded Systems",

    # Product and Design
    "Product Management", "UX/UI Design", "User Research", "Interaction Design", 
    "Product Design", "Prototyping", "Technical Writing", "Information Architecture",

    # Business and Strategy
    "Business Development", "Strategy", "Corporate Development", 
    "Partnerships and Alliances", "Mergers and Acquisitions (M&A)", 
    "Venture and Innovation", "Business Intelligence", "Data Analytics", 
    "Corporate Strategy",

    # Sales, Marketing, and Customer Success
    "Sales", "Sales Engineering", "Account Management", "Customer Success", 
    "Customer Support", "Technical Support", "Customer Experience", 
    "Marketing", "Digital Marketing", "Product Marketing", "Growth Marketing", 
    "Content Marketing", "Branding", "Social Media Marketing", 
    "SEO/SEM", "Public Relations (PR)", "Advertising", "Lead Generation",

    # Operations and Logistics
    "Operations", "IT Operations", "Supply Chain", "Procurement", 
    "Vendor Management", "Logistics", "Facilities Management", 
    "Fulfillment Operations", "Project Management", "Program Management",

    # Financial and Legal
    "Finance", "Accounting", "Corporate Development", "Investor Relations", 
    "Internal Audit", "Compliance", "Legal", "Contract Management", 
    "Risk Management", "Intellectual Property (IP) Management",

    # Human Resources and Administration
    "Human Resources (HR)", "Recruiting/Talent Acquisition", "Learning and Development", 
    "People Operations", "Employee Relations", "Diversity and Inclusion", 
    "Payroll", "Compensation and Benefits", "Organizational Development", 
    "Workplace Experience", "Office Administration",

    # Research and Development
    "Research and Development (R&D)", "Innovation Lab", "Advanced Technologies", 
    "Emerging Technologies", "Artificial Intelligence Research", 
    "Quantum Computing Research", "Blockchain Research",

    # Customer-Facing and Field Departments
    "Field Engineering", "Field Support", "Solutions Engineering", 
    "Solutions Architecture", "Technical Account Management", "Professional Services", 
    "Consulting"
]

# Function to generate a random department name
def get_random_department():
    return random.choice(tech_company_departments)


def generate(amount: int=1):
    for _ in range(amount):
        print('generatin data')
        department = get_random_department()
        department_db_record = Departments( name=department )
        db.session.add(department_db_record)
    db.session.commit()
