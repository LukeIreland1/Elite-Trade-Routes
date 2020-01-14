import requests, json

from EDRoute import EDRoute
from EDStation import EDStation


def get_station_routes(station: EDStation, radius):
    response = json.loads(requests.get("https://www.edsm.net/api-v1/sphere-systems",
                            {"systemName": station.system_name,
                             "radius": radius,
                             "showInformation": 1
                             }).content)

    data = []
    for system in response:
        for buying_station in get_buying_stations(system["name"]):
            data.append(EDRoute(buying_station, station))

    return data

def get_buying_stations(system):
    response = json.loads(requests.get("https://www.edsm.net/api-system-v1/stations",
                                       {"systemName": system
                                        }).content)

    data = []
    for station in response["stations"]:
        if station["economy"] == "Refinery" and station["haveMarket"] is True:
            price_and_supply = get_buying_price_and_supply(system, station["name"])
            data.append(EDStation(station["name"], price_and_supply[0], price_and_supply[1], system))

    return data


def get_buying_price_and_supply(system, station):
    response = json.loads(requests.get("https://www.edsm.net/api-system-v1/stations/market",
                                       {"systemName": system,
                                        "stationName": station
                                        }).content)

    mgf_index = get_mgf_index(response["commodities"])
    mgf = response["commodities"][mgf_index]

    return [mgf["buyPrice"], mgf["stock"]]


def get_mgf_index(commodities):
    counter = 0
    for commodity in commodities:
        if commodity["id"] == "militarygradefabrics":
            return counter
        else:
            counter = counter + 1
    return 0
