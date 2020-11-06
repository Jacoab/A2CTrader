class EnvironmentAlphaModel(AlphaModel):

    def __init__(self):
        self.environment = []

    def OnSecuritiesChanges(self, algorithm, changes):
        pass

    def Update(self, algorithm, data):
        pass

    def ShouldEmitInsight(self):
        pass


class Environment(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2009, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 1, 31)
        self.SetCash(100000)  # Set Strategy Cash

        self.symbols = [Symbol.Create("TSLA", SecurityType.Equity, Market.USA),
                        Symbol.Create("AAPL", SecurityType.Equity, Market.USA),
                        Symbol.Create("IBM", SecurityType.Equity, Market.USA),
                        Symbol.Create("GOOGL", SecurityType.Equity, Market.USA),
                        Symbol.Create("AMZN", SecurityType.Equity, Market.USA)]

        self.SetUniverseSelection(ManualUniverseSelectionModel(self.symbols))

    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''

        # if not self.Portfolio.Invested:
        #    self.SetHoldings("SPY", 1)
        pass
