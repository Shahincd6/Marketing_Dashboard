import pandas as pd
import numpy as np

def load_and_process_data():
    """Load and process all marketing and business data"""
    
    # Load CSV files
    facebook = pd.read_csv('dataset/Facebook.csv')
    google = pd.read_csv('dataset/Google.csv')
    tiktok = pd.read_csv('dataset/TikTok.csv')
    business = pd.read_csv('dataset/business.csv')
    
    # Add platform and combine
    facebook['platform'] = 'Facebook'
    google['platform'] = 'Google'
    tiktok['platform'] = 'TikTok'
    marketing_data = pd.concat([facebook, google, tiktok], ignore_index=True)
    
    # Convert dates
    marketing_data['date'] = pd.to_datetime(marketing_data['date'])
    business['date'] = pd.to_datetime(business['date'])
    
    # Calculate key metrics
    marketing_data['ctr'] = (marketing_data['clicks'] / marketing_data['impression'] * 100).round(2)
    marketing_data['cpc'] = (marketing_data['spend'] / marketing_data['clicks']).round(2)
    marketing_data['roas'] = (marketing_data['attributed revenue'] / marketing_data['spend']).round(2)
    marketing_data['cpm'] = (marketing_data['spend'] / (marketing_data['impression'] / 1000)).round(2)
    
    business['avg_order_value'] = (business['total revenue'] / business['# of orders']).round(2)
    business['customer_acquisition_rate'] = (business['new customers'] / business['# of orders'] * 100).round(2)
    
    return marketing_data, business