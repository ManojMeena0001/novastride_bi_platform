"""
Module: nlp_analysis.py
Description: Extracts raw e-commerce customer reviews from MySQL, executes
             lexicon-based sentiment scoring, and classifies operational complaints.
"""
import pandas as pd
import nltk
import pandas as pd
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

def analyze_and_classify_text(df:pd.DataFrame)->pd.DataFrame:
    """
    Processes raw text reviews using VADER scoring and assigns 
    discrete operational category classifications.
    """
    if df.empty:
        return df
    sia=SentimentIntensityAnalyzer()

    sentiments=[]
    scores=[]
    categories=[]

    for _, row in df.iterrows():
        text=str(row['review_text'])
        text_lower=text.lower()

        # Run Vader Sentiment Polarity Analysis .
        polarity_scores=sia.polarity_scores(text)
        compound_scores=polarity_scores['compound']
        scores.append('compound_score')


        # Categorize text based on standard retail analytics thresholds
        if compound_scores>=0.05:
            sentiments.append('positive')
        elif compound_scores<=-0.05:
            sentiments.append("negative")
        else:
            sentiments.append('neutral')

    # 2. Rule-Based Classification Matrix (Mapping Text to Business Departments)
    if any(word in text_lower for word in ['shipping', 'delivery', 'took too long', 'delayed']):
        categories.append('shipping delay')

    elif any(word in text_lower for word in ['quality', 'fabric', 'stitching', 'material']):
        categories.append('product quality issues')
    elif  any(word in text_lower for word in ['damaged', 'package', 'packaging', 'broken']):
        categories.append('packaging defect ')
    elif any(word in text_lower for word in ['refund', 'return', 'different', 'image']):
        categories.append('recieved wrong item ')
    else:
        categories.append('due to general_enquiry')
    

    # Append the calculated matrix rows into the DataFrame payload
    df['ai_sentiment'] = sentiments
    df['ai_sentiment_score'] = scores
    df['ai_issue_category'] = categories
    
    return df
