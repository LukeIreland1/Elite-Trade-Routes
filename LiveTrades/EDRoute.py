from EDStation import EDStation


class EDRoute:

    def __init__(self, buying: EDStation, selling: EDStation):
        self.buying = buying
        self.selling = selling
        self.profit = selling.price - buying.price

    def __str__(self):
        return "profit: " + str(self.profit) + " | " + \
               str(self.buying.station_name) + " | " + \
                str(self.selling.station_name)
