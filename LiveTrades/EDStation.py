class EDStation:

    def __init__(self, station_name, price, quantity, system_name):
        self.station_name = station_name
        self.price = price
        self.quantity = quantity
        self.system_name = system_name

    def __str__(self):
        return "{station_name=" + self.station_name + \
               ", price=" + str(self.price) + \
               ", quantity=" + str(self.quantity) + \
               ", system_name=" + self.system_name + "}"
