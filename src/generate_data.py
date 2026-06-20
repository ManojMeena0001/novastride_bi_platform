import pandas as pd
import random
from db_connect import get_db_connection
from datetime import timedelta
from faker import Faker

# Initialize Faker
fake = Faker()


def generate_ecom_data(num_customers=100, num_transactions=300):

    # =========================================================================
    # STAGE 1: CUSTOMER GENERATION
    # =========================================================================

    customers = []

    cities = [
        'Bengaluru', 'Pune', 'Hyderabad', 'Delhi',
        'Mumbai', 'Indore', 'Chennai', 'Kolkata',
        'Bhubaneshwar', 'Ahmedabad', 'Dehradun',
        'Nagpur', 'Thiruvananthapuram'
    ]

    for i in range(1, num_customers + 1):

        name = fake.name()

        email = (
            f"{name.lower().replace(' ', '')}"
            f"@{fake.free_email_domain()}"
        )

        signup_date = fake.date_between(
            start_date='-1y',
            end_date='today'
        )

        customers.append({
            'customer_id': i,
            'customer_name': name,
            'email': email,
            'signup_date': signup_date,
            'city': random.choice(cities)
        })

    df_customers = pd.DataFrame(customers)
    #===================================================================
    #    Product Details Generation 
    #===================================================================
    products = []

    categories = [
        'Electronics',
        'Fashion',
        'Home',
        'Beauty',
        'Sports'
    ]

    for p_id in range(101, 151):

        products.append({
            'product_id': p_id,
            'product_name': f'Product_{p_id}',
            'category': random.choice(categories),
            'price': random.choice([299,399,499,599,699]),
            'stock_quantity': random.randint(10,200)
        })

    df_products = pd.DataFrame(products)

    # =========================================================================
    # STAGE 2: TRANSACTION GENERATION
    # =========================================================================

    transactions = []

    statuses = [
        'Delivered',
        'Delivered',
        'Delivered',
        'Cancelled',
        'Returned'
    ]

    for t_id in range(1, num_transactions + 1):

        cust_id = random.choice(df_customers['customer_id'].tolist())

        prod_id = random.randint(101, 150)

        purchase_date = fake.date_time_between(
            start_date='-6m',
            end_date='now'
        )

        quantity = random.randint(1, 4)

        unit_price = random.choice([
            299,
            399,
            499,
            599,
            699
        ])

        total_amount = quantity * unit_price

        order_status = random.choice(statuses)

        transactions.append({
            'transaction_id': t_id,
            'customer_id': cust_id,
            'product_id': prod_id,
            'purchase_date': purchase_date,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_amount': total_amount,
            'orderstatus': order_status
        })

    df_transactions = pd.DataFrame(transactions)

    # =========================================================================
    # STAGE 3: CUSTOMER FEEDBACK GENERATION
    # =========================================================================

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

        # About 60% customers leave reviews
        if random.random() > 0.4:

            t_id = row['transaction_id']
            status = row['orderstatus']
            p_date = row['purchase_date']

            if status in ['Cancelled', 'Returned']:
                text = random.choice(complaints)

            else:
                text = (
                    random.choice(praises)
                    if random.random() > 0.2
                    else random.choice(complaints)
                )

            review_date = p_date + timedelta(
                days=random.randint(1, 7)
            )

            feedback.append({
                'feedback_id': f_id,
                'transaction_id': t_id,
                'review_text': text,
                'review_date': review_date,
                'ai_sentiment': None,
                'ai_sentiment_score': None,
                'ai_issue_category': None
            })

            f_id += 1

    df_feedback = pd.DataFrame(feedback)

    return (
        df_customers,
        df_products,
        df_transactions,
        df_feedback
    )


# =========================================================================
# MAIN EXECUTION
# =========================================================================

if __name__ == "__main__":

    engine = get_db_connection()

    if engine:

        df_cust,df_prod, df_trans, df_feed = generate_ecom_data()

        print(
            f"✅ Data Matrices Synthesized: "
            f"{len(df_cust)} Customers | "
            f"{len(df_trans)} Transactions | "
            f"{len(df_feed)} Reviews."
        )

        print("\n Sample Unstructured Review Text Preview:\n")
        #-----------------------------------------------------------------------------
        #     Bulk Data Ingestion 
        #-----------------------------------------------------------------------------
        print('Commencing Bulk Database Ingestion layer .....')
        try:
            # Load Customers first (Primary Key dimension base)
            # if_exists='append' ensures we add new rows without dropping the table structure
            # index=False prevents Pandas from creating an accidental extra index column in SQL
            df_cust.to_sql(name='dim_customers',con=engine,if_exists='append',index=False)
            print(" Successfully ingested records into table: dim_customers")

            df_prod.to_sql(name='dim_products',con=engine,if_exists='append',index=False)

            print(" Successfully ingested records into table: dim_products")


            # Load Transactions second (Dependent Foreign Key fact set)
            df_trans.to_sql(name='fact_transactions', con=engine, if_exists='append', index=False)
            print(" Successfully ingested records into table: fact_transactions")
            
            print("\n🎉 Success: Database synchronization completely flawless!")
            df_feed.to_sql(name='fact_customer_feedback',con=engine,if_exists='append',index=False)

            print("💾 Successfully ingested records into table: fact_customer_feedback")
        except Exception as e:
            print(f"\nIngestion Layer Failed. Database rolled back. Error details: {e}")