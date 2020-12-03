import quandl
from dotenv import load_dotenv
import os


load_dotenv()

quandl.ApiConfig.api_key = os.getenv('QUANDL_KEY')

start_date = "2010-01-01"
end_date = "2020-01-01"

print('Starting data collection...')
amazon_data = quandl.get('WIKI/AMD', start_date=start_date, end_date=end_date)
shopify_data = quandl.get('WIKI/NVDA', start_date=start_date, end_date=end_date)

print('Writing data to disk...')
amazon_data.to_csv('amd')
shopify_data.to_csv('nvidia')
