import requests
from bs4 import BeautifulSoup
from EDStation import EDStation


def get_selling_stations():
    page = BeautifulSoup(requests.get("https://eddb.io/commodity/304").content, "html.parser")

    row = page.find("table", {"id": "table-stations-max-sell"}) \
        .find_next("tbody") \
        .find_next("tr")

    data = []
    while row is not None:
        station_name = row.find_next("td") \
            .find_next("a").next

        system_name = row.find_next("td") \
            .find_next_sibling("td") \
            .find_next("a").next

        price = clean_number(str(row.find_next("td") \
            .find_next_sibling("td") \
            .find_next_sibling("td") \
            .find_next("span").next))

        demand = clean_number(str(row.find_next("td") \
            .find_next_sibling("td") \
            .find_next_sibling("td") \
            .find_next_sibling("td") \
            .find_next_sibling("td") \
            .find_next("span").next))

        data.append(EDStation(station_name, price, demand, system_name))

        row = row.find_next_sibling("tr")

    return data


def clean_number(string):
    return int(string.replace(",", ""))
