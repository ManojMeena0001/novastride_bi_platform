import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
from db_connect import get_db_connection

# Initialize Faker with English locale data
fake = Faker()

def generate_customers(num_customers=100):
    """
    Generates a list of dictionary entries matching the dim_customers schema.
    """
    customers = []
    
    # Common Indian e-commerce target markets for realistic data profiling
    cities = ['Bhopal', 'Mumbai', 'Delhi', 'Bangalore', 'Pune', 'Hyderabad']
    
    for _ in range(num_customers):
        name = fake.name()
        # Generate a clean lowercase email using the customer's name
        email = f"{name.lower().replace(' ', '')}@{fake.free_email_domain()}"
        
        # Generate a random signup date over the past year
        signup_date = fake.date_between(start_date='-1y', end_date='today')
        city = random.choice(cities)
        
        customers.append({
            "customer_name": name,
            "email": email,
            "signup_date": signup_date,
            "city": city
        })
    
    return pd.DataFrame(customers)

if __name__ == "__main__":
    # 1. Connect to our verified database
    engine = get_db_connection()
    
    if engine:
        print("🚀 Starting Data Generation Pipeline...")
        
        # 2. Generate and display our customer data batch
        df_customers = generate_customers(100)
        print(f"📊 Previewing {len(df_customers)} generated customer records:")
        print(df_customers.head())