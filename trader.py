from environment import ActionType, Environment
import pandas as pd


amazon = pd.read_csv('amazon')
nvidia = pd.read_csv('nvidia')

amazon.name = 'AMZN'
nvidia.name = 'NVDA'

env = Environment(10000, 1, amazon, nvidia)
'''
print(env.state)
print(env.holdings_range[0])
print(env.holdings_range[1])
print(env.state[env.holdings_range[0], env.holdings_range[1]])
'''
funds = env.get_funds()
holdings = env.get_holdings()
print('Start')
print('Funds: ${}'.format(funds))
print('Holdings: AMZN: {}, NVDA: {}'.format(holdings[0], holdings[1]))
print()

state = env.step(ActionType.BUY, 'AMZN', 1)
funds = env.get_funds()
holdings = env.get_holdings()
print('Step 1')
print('State: {}'.format(state))
print('Funds: ${}'.format(funds))
print('Holdings: AMZN: {}, NVDA: {}'.format(holdings[0], holdings[1]))
print()

state = env.step(ActionType.SELL, 'AMZN', 1)
funds = env.get_funds()
holdings = env.get_holdings()
print('Step 2')
print('State: {}'.format(state))
print('Funds: ${}'.format(funds))
print('Holdings: AMZN: {}, NVDA: {}'.format(holdings[0], holdings[1]))
print()
