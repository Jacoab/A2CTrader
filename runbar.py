class RunBar(AlphaModel):

    def __init__(self,
                 volumeType=True,
                 movingAverageType=MovingAverageType.Exponential,
                 resolution=Resolution.Daily):
        self.volumeType = volumeType
        self.movingAverageType = movingAverageType
        self.resolution = resolution
        self.symbolData = {}

    def Update(self, algorithm, changes):
        pass

    def OnSecuritiesChanged(self, algorithm, changes):
        pass