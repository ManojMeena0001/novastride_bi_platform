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

# =========================================================================
# STAGE 2: FACT_TRANSACTIONS GENERATION
# =========================================================================

    transactions=[]
    status=['Delivered', 'Delivered', 'Delivered', 'Cancelled', 'Returned']
    for t_id in range(1,num_customers+1):
        cust_id=random.choice(df_customers['customer_id'])
        prod_id=random.randint(101,150)
        purchase_date=fake.date_time_between(start_date='-6m',end_date='today')
        quantity=random.randint(1,4)
        unit_price=random.choice([499,399,299,599,699])
        total_amount=quantity*unit_price
        order_status=random.choice(status)
        transactions.append({
            'transaction_id': t_id,
            'customer_id': cust_id,
            'product_id': prod_id,
            'purchase_date': purchase_date,
            'quantity': quantity,
            'total_amount': total_amount,
            'orderstatus': order_status
        })

    df_transactions = pd.DataFrame(transactions)

# # STAGE 3: FACT_CUSTOMER_FEEDBACK GENERATION (NLP BASE)

    feedback = []
    f_id = 1
    
    complaints = [
        "The size was completely wrong and shipping took way too long. Disappointed.",
        "Fabric quality is highly subpar. The stitching started coming apart after the first wash.",
        "Horrible delivery experience. Package was completely damaged when it arrived.",
        "Product looks entirely different from the online store image. Initiated a refund request."
    ]
    praises = [
        "Absolutely amazing fit! The fabric quality feels highly premium. Will order again.",
        "Super fast delivery and the product packaging was exceptionally clean.",
        "Very comfortable material. Completely worth the price point.",
        "Excellent customer support team and great product design."
    ]
    
    for _, row in df_transactions.iterrows():
        if random.random() > 0.4:  
            t_id = row['transaction_id']
            status = row['orderstatus']
            p_date = row['purchase_date']
            
            if status in ['Cancelled', 'Returned']:
                text = random.choice(complaints)
            else:
                text = random.choice(praises) if random.random() > 0.2 else random.choice(complaints)
            
            review_date = p_date + timedelta(days=random.randint(1, 7))
            
            feedback.append({
                "feedback_id": f_id,
                "transaction_id": t_id,
                "review_text": text,
                "review_date": review_date,
                "ai_sentiment": None,         
                "ai_sentiment_score": None,  
                "ai_issue_category": None     
            })
            f_id += 1


if __name__ =='__main__':
    #Initialise the verification connection handshake from utils 
    engine = get_db_connection()
    if engine:  
        if_cust, df_trans, df_feed = generate_ecom_data()
            
        print(f"✅ Data Matrices Synthesized: {len(df_cust)} Customers | {len(df_trans)} Transactions | {len(df_feed)} Reviews.")
        print("\n📝 Sample Unstructured Review Text Preview:")
        print(df_feed[['transaction_id', 'review_text']].head())