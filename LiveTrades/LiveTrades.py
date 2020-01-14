import Scraper, API

radius = 10

for station in Scraper.get_selling_stations():
    for route in API.get_station_routes(station, radius):
        print(route)