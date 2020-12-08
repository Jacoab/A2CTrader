import quandl
from dotenv import load_dotenv
import os


load_dotenv()

quandl.ApiConfig.api_key = os.getenv('QUANDL_KEY')

train_start_date = "2002-01-01"
train_end_date = "2010-01-01"
test_start_date = "2010-05-01"
test_end_date = "2020-01-01"

print('Starting data collection...')
train_swk_data = quandl.get('WIKI/AMD', start_date=train_start_date, end_date=train_end_date)
train_aap_data = quandl.get('WIKI/NVDA', start_date=train_start_date, end_date=train_end_date)
test_swk_data = quandl.get('WIKI/AMD', start_date=test_start_date, end_date=test_end_date)
test_aap_data = quandl.get('WIKI/NVDA', start_date=test_start_date, end_date=test_end_date)

print('Writing data to disk...')
train_swk_data.to_csv('amd-train.csv')
train_aap_data.to_csv('nvda-train.csv')
test_swk_data.to_csv('amd-test.csv')
test_aap_data.to_csv('nvda-test.csv')


print('amd length: ', len(test_swk_data['Open']))
print('nvda length: ', len(test_aap_data['Open']))
