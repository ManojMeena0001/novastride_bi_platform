import pandas as pd
import random
from db_connect import get_db_connection
from datetime import datetime , timedelta
from faker import Faker
# Initialise faker 
fake=Faker()


def generate_ecom_data(num_customers=100,num_transactions=300):
    # Generates structured relational data matrices matching your SQL Schema perfectly.
    customers=[]
    cities = ['Bengaluru','Pune','Hyderabad','Delhi','Mumbai','Indore','Chennai','Kolkata','Bhubaneshwar','Ahemadabad','Dehradun','Nagpur','Thiruvanantpuram']
    for i in range(1,num_customers+1):
        name=fake.name()
        # Clean processing: lowercase names and strip whitespaces for standard email sanitization# Clean processing: lowercase names and strip whitespaces for standard email sanitization
        email=f'{name.lower().replace(' ','')}@{fake.free_email_domain()}'
        signup_date=fake.date_between(start_date='-1y',end_date='today')
    customers.append({'customer_id':i,
                      'customer_name':name,
                      'email':email,
                      'signup_date':signup_date,
                      'city':random.choice(cities)})
    df_customers=pd.DataFrame(customers)


