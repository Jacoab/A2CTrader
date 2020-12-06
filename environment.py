import random

import numpy as np
from enum import Enum


#class ActionType(Enum):
#    BUY = 0
#    SELL = 1
#    HOLD = 2


ActionType = ['BUY', 'SELL', 'HOLD', '']


class Environment:

    def __init__(self, funds, max_shares, *argv):
        self.step_num = 0
        self.day_index = self.step_num + 4

        holdings = [0 for _ in argv]
        opening_prices = [arg['Open'][self.day_index] for arg in argv]
        opening_avgs = [0.0 for _ in argv]

        self.share_amounts = [i for i in range(max_shares + 1)]

        self.init_funds = funds
        self.buyable_stocks = {stock.name: stock for stock in argv}
        self.holdings_name_list = list(self.buyable_stocks.keys())
        self.num_of_equities = len(argv)
        self.prev_5_opens = np.array([stock['Open'][0:5] for stock in argv])

        self.state = np.array([funds, 0.0] + holdings + opening_prices + opening_avgs)
        self.holdings_range = (2, 2 + len(argv))
        self.opening_prices_range = (self.holdings_range[1],
                                     self.holdings_range[1] + self.num_of_equities)
        self.opening_avgs_range = (self.opening_prices_range[1],
                                   self.opening_prices_range[1] + self.num_of_equities)

        self.set_past_5_days_open_avg(self.calc_past_5_days_open_avg())

    '''
    def reset(self, funds):
        holdings = [0 for _ in range(self.num_of_equities)]
        opening_prices = [stock['Open'][0] for stock in self.buyable_stocks]
        opening_avgs = [0.0 for _ in range(self.num_of_equities)]

        self.state = np.array([self.init_funds, 0.0] + holdings + opening_prices + opening_avgs)
        self.step = 0
    '''

    def step(self, action_type, stock, amount_of_shares):
        if action_type not in ActionType:
            raise ValueError('{} is not a valid action type'.format(action_type))
        if amount_of_shares not in self.share_amounts:
            raise ValueError('{} is not a valid amount of shares to buy'.format(amount_of_shares))

        if action_type == 'HOLD':
            reward = self.calc_sparse_reward(self.get_funds())
            return self.state, reward, False

        price_per_share = self.buyable_stocks[stock]['Open'][self.day_index]
        holdings = self.get_holdings()
        holdings_index = self.holdings_name_list.index(stock)
        funds = self.get_funds()

        if action_type == 'BUY':
            if price_per_share*amount_of_shares >= funds:
                return np.array([]), 0.0, True
            else:
                self.buy(stock, amount_of_shares, price_per_share)
        elif action_type == 'SELL':
            if amount_of_shares > holdings[holdings_index]:
                return np.array([]), 0.0, True
            else:
                self.sell(stock, amount_of_shares, price_per_share)
        else:
            pass

        self.step_num += 1
        self.day_index += 1

        new_opens = np.array([stock['Open'][self.day_index] for stock in self.buyable_stocks.values()])
        self.set_opening_prices(new_opens)
        self.push_prev_5_opens(new_opens)
        past_5_day_avgs = self.calc_past_5_days_open_avg()
        self.set_past_5_days_open_avg(past_5_day_avgs)

        reward = self.calc_sparse_reward(funds)

        return self.state, reward, False

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

    def calc_sparse_reward(self, prev_funds):
        return (self.get_funds() - prev_funds) / self.init_funds

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
