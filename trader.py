from environment import ActionType, Environment
import pandas as pd


amazon = pd.read_csv('amazon')
nvidia = pd.read_csv('nvidia')

amazon.name = 'AMZN'
nvidia.name = 'NVDA'

env = Environment(10000, 1, amazon, nvidia)
print('Start')
print('Funds: $', env.get_funds())
print('Portfolio value: ', env.get_portfolio_val())
print('Holdings: AMZN: {}, NVDA: {}'.format(env.get_holdings()[0], env.get_holdings()[1]))
print('Opens: AMZN=${}, NVIDIA=${}'.format(env.get_opening_prices()[0], env.get_opening_prices()[1]))
print('5 Day Averages: AMZN=${}, NVDA=${}'.format(env.get_past_5_days_open_avg()[0], env.get_past_5_days_open_avg()[1]))
print()

state = env.step(ActionType.BUY, 'AMZN', 1)
print('Step 1')
print('State: ', state)
print('Funds: $', env.get_funds())
print('Portfolio value: ', env.get_portfolio_val())
print('Holdings: AMZN: {}, NVDA: {}'.format(env.get_holdings()[0], env.get_holdings()[1]))
print('Opens: AMZN=${}, NVIDIA=${}'.format(env.get_opening_prices()[0], env.get_opening_prices()[1]))
print('5 Day Averages: AMZN=${}, NVDA=${}'.format(env.get_past_5_days_open_avg()[0], env.get_past_5_days_open_avg()[1]))
print()

state = env.step(ActionType.SELL, 'AMZN', 1)
print('Step 2')
print('State: ', state)
print('Funds: $', env.get_funds())
print('Portfolio value: ', env.get_portfolio_val())
print('Holdings: AMZN: {}, NVDA: {}'.format(env.get_holdings()[0], env.get_holdings()[1]))
print('Opens: AMZN=${}, NVIDIA=${}'.format(env.get_opening_prices()[0], env.get_opening_prices()[1]))
print('5 Day Averages: AMZN=${}, NVDA=${}'.format(env.get_past_5_days_open_avg()[0], env.get_past_5_days_open_avg()[1]))
print()

state = env.step(ActionType.BUY, 'NVDA', 1)
print('Step 3')
print('State: ', state)
print('Funds: $', env.get_funds())
print('Portfolio value: ', env.get_portfolio_val())
print('Holdings: AMZN: {}, NVDA: {}'.format(env.get_holdings()[0], env.get_holdings()[1]))
print('Opens: AMZN=${}, NVIDIA=${}'.format(env.get_opening_prices()[0], env.get_opening_prices()[1]))
print('5 Day Averages: AMZN=${}, NVDA=${}'.format(env.get_past_5_days_open_avg()[0], env.get_past_5_days_open_avg()[1]))
print()
