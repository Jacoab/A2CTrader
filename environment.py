import random
import numpy as np


ActionType = ['BUY', 'SELL', 'HOLD', '']


class Environment:

    def __init__(self, funds, max_shares, trial_len, *argv):
        n = random.randint(0, len(argv[0]) - trial_len)  # Starting point for random sampling of stock open sequences
        # THis helps prevent overfitting

        self.step_num = 0
        self.day_index = n + 4   # Keeps track of place in stock dataframes with offset=4 for 5 day averages
        self.init_day_index = self.day_index

        holdings = [0 for _ in argv]
        opening_prices = [arg['Open'][self.day_index] for arg in argv]
        opening_avgs = [0.0 for _ in argv]

        self.share_amounts = [i for i in range(max_shares + 1)]

        self.init_funds = funds
        self.buyable_stocks = {stock.name: stock for stock in argv}
        self.holdings_name_list = list(self.buyable_stocks.keys())
        self.num_of_equities = len(argv)
        self.prev_5_opens = np.array([stock['Open'][n:n+5] for stock in argv])

        self.state = np.array([funds, 0.0] + holdings + opening_prices + opening_avgs)

        # Ranges for indexing each subset of the state, used in getter/setter methods
        self.holdings_range = (2, 2 + len(argv))
        self.opening_prices_range = (self.holdings_range[1],
                                     self.holdings_range[1] + self.num_of_equities)
        self.opening_avgs_range = (self.opening_prices_range[1],
                                   self.opening_prices_range[1] + self.num_of_equities)

        self.set_past_5_days_open_avg(self.calc_past_5_days_open_avg())

    # Steps through each day of prices in stock dataframes
    def step(self, action_type, stock, amount_of_shares):
        if action_type not in ActionType:
            raise ValueError('{} is not a valid action type'.format(action_type))
        if amount_of_shares not in self.share_amounts:
            raise ValueError('{} is not a valid amount of shares to buy'.format(amount_of_shares))

        # If action is hold update state and continue
        if action_type == 'HOLD':
            reward = self.partial_update_state(self.get_funds())
            return self.state, reward, False

        price_per_share = self.buyable_stocks[stock]['Open'][self.day_index]
        holdings = self.get_holdings()
        holdings_index = self.holdings_name_list.index(stock)
        funds = self.get_funds()

        if action_type == 'BUY':
            # Check to see if agent buys more shares than it can afford
            if price_per_share*amount_of_shares >= funds:
                return self.state, 0.0, True
            else:
                self.buy(stock, amount_of_shares, price_per_share)
        elif action_type == 'SELL':
            # CHeck to see if agent sells more shares than it owns
            if amount_of_shares > holdings[holdings_index]:
                return self.state, 0.0, True
            else:
                self.sell(stock, amount_of_shares, price_per_share)
        else:
            pass

        reward = self.partial_update_state(funds)
        return self.state, reward, False

    # Updates state values unaffected by which action is taken
    def partial_update_state(self, funds):
        self.step_num += 1
        self.day_index += 1

        new_opens = np.array([stock['Open'][self.day_index] for stock in self.buyable_stocks.values()])
        self.set_opening_prices(new_opens)
        self.push_prev_5_opens(new_opens)
        past_5_day_avgs = self.calc_past_5_days_open_avg()
        self.set_past_5_days_open_avg(past_5_day_avgs)

        reward = self.calc_complex_reward(funds)
        return reward

    # Buys stock and updates state
    def buy(self, stock, shares, price_per_share):
        funds = self.get_funds()
        holdings = self.get_holdings()
        holdings_index = self.holdings_name_list.index(stock)

        funds -= shares * price_per_share
        holdings[holdings_index] = holdings[holdings_index] + shares

        self.set_funds(funds)
        self.set_holdings(holdings)
        portfolio_val = self.calc_portfolio_value()
        self.set_portfolio_val(portfolio_val)

    # Sells stock and updates state
    def sell(self, stock, shares, price_per_share):
        funds = self.get_funds()
        holdings = self.get_holdings()
        holdings_index = self.holdings_name_list.index(stock)

        funds += shares * price_per_share
        holdings[holdings_index] = holdings[holdings_index] - shares

        self.set_funds(funds)
        self.set_holdings(holdings)
        portfolio_val = self.calc_portfolio_value()
        self.set_portfolio_val(portfolio_val)

    def hold(self):
        # NOTE: This method might not be necessary
        pass

    # Simple sparse reward
    def calc_sparse_reward(self, prev_funds):
        reward = (self.get_funds() - prev_funds) / self.init_funds

        if reward > 0:
            reward += 1    # positive rewards are rare so they should be worth more

        return reward

    # Better reward function
    def calc_complex_reward(self, prev_funds):
        reward = (self.get_funds() - prev_funds) / self.init_funds
        averages = self.get_past_5_days_open_avg()
        opens = self.get_opening_prices()
        holdings = self.get_holdings()

        if reward > 0:
            reward += 1.0    # positive rewards are rare so they should be worth more

        holdings_values = opens * holdings
        average_holdings = averages * holdings

        for i in range(self.num_of_equities):
            if holdings_values[i] > average_holdings[i]:
                reward += 0.5

        return reward

    def calc_portfolio_value(self):
        value = 0.0
        holdings_index = self.holdings_range[0]
        openings_index = self.opening_prices_range[0]
        for _ in range(self.num_of_equities):
            value += self.state[holdings_index] * self.state[openings_index]
            holdings_index += 1
            openings_index += 1

        return value

    def calc_past_5_days_open_avg(self):
        return np.array([np.average(opens) for opens in self.prev_5_opens])

    # Adds new open to the past 5 day opens moving window
    # Used to calculate the moving average
    def push_prev_5_opens(self, new_opens):
        self.prev_5_opens = np.roll(self.prev_5_opens, 1, 1)
        self.prev_5_opens[:, 0] = new_opens

    def set_funds(self, funds):
        self.state[0] = truncate(funds, 2) # Possibly round instead

    def set_portfolio_val(self, value):
        self.state[1] = value # NOTE: Possibly round to two decimal places???

    def set_holdings(self, holdings):
        self.state[self.holdings_range[0]: self.holdings_range[1]] = holdings

    def set_opening_prices(self, opening_prices):
        self.state[self.opening_prices_range[0]: self.opening_prices_range[1]] = opening_prices

    def set_past_5_days_open_avg(self, avgs):
        trunc_avgs = np.array([truncate(val, 2) for val in avgs])
        self.state[self.opening_avgs_range[0]: self.opening_avgs_range[1]] = trunc_avgs

    def get_funds(self):
        return self.state[0]

    def get_portfolio_val(self):
        return self.state[1]

    def get_holdings(self):
        return self.state[self.holdings_range[0]: self.holdings_range[1]]

    def get_opening_prices(self):
        return self.state[self.opening_prices_range[0]: self.opening_prices_range[1]]

    def get_past_5_days_open_avg(self):
        return self.state[self.opening_avgs_range[0]: self.opening_avgs_range[1]]


def sample_action_space():
    return random.choice(ActionType)


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))
