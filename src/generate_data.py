import random 
import pandas as pd 
from datetime import datetime,timedelta
from faker import Faker
from db_connect import get_db_connection

fake=Faker()

def generate_customers(num_customers=100):   #  function made for customer data generation
    
    customers=[]

    cities=['Bengaluru','Pune','Hyderabad','Delhi','Mumbai','Indore','Chennai','Kolkata','Bhubaneshwar','Ahemadabad','Dehradun','Nagpur','Thiruvanantpuram']

    for _ in range(num_customers):
        name=fake.name()
        email=f"{name.lower().replace(' ','')}@{fake.free_email_domain()}"
        signup_date=fake.date_between(start_date='-1y',end_date='today')
        city=random.choice(cities)

        customers.append({'customer_name':name,
                          'email':email,
                          'signup_date':signup_date,
                          'city':city
                          })
    return pd.DataFrame(customers)




#------------------------------------------------------



if __name__ == "__main__" :
    engine=get_db_connection()
    if engine:
        print('🚀 Starting Data Generation Pipeline .... ')
        df_customers=pd.DataFrame(generate_customers(100))
        print(f"📊 Previewing {len(df_customers)} generated customer records:")
        print(df_customers.head())