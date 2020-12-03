import numpy as np
from enum import Enum


class ActionType(Enum):
    BUY = 0
    SELL = 1
    HOLD = 2


class Environment:

    def __init__(self, funds, max_shares, *argv):
        holdings = [0 for _ in argv]
        opening_prices = [arg['Open'][0] for arg in argv]
        opening_avgs = [0.0 for _ in argv]

        self.share_amounts = [i for i in range(max_shares + 1)]

        self.init_funds = funds
        self.buyable_stocks = {stock.name: stock for stock in argv}
        self.holdings_name_list = list(self.buyable_stocks.keys())
        self.num_of_equities = len(argv)
        self.prev_5_opens = np.zeros([self.num_of_equities, 5])

        self.state = np.array([funds, 0.0] + holdings + opening_prices + opening_avgs)
        self.holdings_range = (2, 2 + len(argv))
        self.opening_prices_range = (self.holdings_range[1] + 1,
                                     self.holdings_range[1] + 1 + self.num_of_equities)
        self.opening_avgs_range = (self.opening_prices_range[1] + 1,
                                   self.opening_prices_range[1] + 1 + self.num_of_equities)

        self.step_num = 0
        self.episode = 0

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

        price_per_share = self.buyable_stocks[stock]['Open'][self.step_num]
        holdings = self.get_holdings()
        holdings_index = self.holdings_name_list.index(stock)
        funds = self.get_funds()

        print('STEP:')
        print('  ', holdings[holdings_index])
        print('  ', price_per_share*amount_of_shares)
        print('  ', funds)

        if action_type == ActionType.BUY:
            print(price_per_share*amount_of_shares)
            if price_per_share*amount_of_shares >= funds:
                return None
            else:
                self.buy(stock, amount_of_shares, price_per_share)
        elif action_type == ActionType.SELL:
            if amount_of_shares > holdings[holdings_index]:
                return None
            else:
                self.sell(stock, amount_of_shares, price_per_share)
        else:
            pass

        self.step_num += 1
        new_opens = np.array([stock['Open'][self.step_num] for stock in self.buyable_stocks.values()])
        self.set_opening_prices(new_opens)
        self.push_prev_5_opens(new_opens)
        return self.state

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
        self.state[0] = funds

    def set_portfolio_val(self, value):
        self.state[1] = value

    def set_holdings(self, holdings):
        self.state[self.holdings_range[0]: self.holdings_range[1]] = holdings

    def set_opening_prices(self, opening_prices):
        self.state[self.opening_prices_range[0]: self.opening_prices_range[1]] = opening_prices

    def set_past_5_days_open_avg(self, avgs):
        self.state[self.opening_avgs_range[0]: self.opening_avgs_range[1]] = avgs

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
