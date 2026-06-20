"""
Module: nlp_analysis.py
Description: Extracts raw e-commerce customer reviews from MySQL, executes
             lexicon-based sentiment scoring, and classifies operational complaints.
"""
import pandas as pd
import nltk
from db_connect import get_db_connection
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon dependencies silently into the environment.
nltk.download('vader_lexicon',quiet=True)
def fetch_raw_reviews(engine) ->pd.DataFrame:
    query="""
            select feedback_id,
                    transaction_id,
                    review_text    
                    from fact_customer_feedback 
            where ai_sentiment IS NULL
            
        """
    
    return pd.read_sql(query,con=engine)

if __name__=="__main__":
    engine=get_db_connection()
    if engine :
        print('Initialising NLP Engine Sentiment Pipeline .')
        df_reviews = fetch_raw_reviews(engine)
        print(f"Successfully extracted {len(df_reviews)} raw records waiting for ai classification")
    
    
