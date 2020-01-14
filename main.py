import csv
import json
import sys
import urllib.request
from pathlib import Path
from urllib.request import urlretrieve
from operator import itemgetter
import pandas as pd
import pickle

ROOT = Path(__file__).parent

SYSTEMS_URL = "https://eddb.io/archive/v6/systems.csv"
UPDATED_SYSTEMS_URL = "https://eddb.io/archive/v6/systems_recently.csv"
POPULATED_SYSTEMS_URL = "https://eddb.io/archive/v6/systems_populated.json"
BODIES_URL = "https://eddb.io/archive/v6/bodies.jsonl"
UPDATED_BODIES_URL = "https://eddb.io/archive/v6/bodies_recently.jsonl"
STATIONS_URL = "https://eddb.io/archive/v6/stations.json"
FACTIONS_URL = "https://eddb.io/archive/v6/factions.json"
LISTINGS_URL = "https://eddb.io/archive/v6/listings.csv"
COMMODITIES_URL = "https://eddb.io/archive/v6/commodities.json"
MODULES_URL = "https://eddb.io/archive/v6/modules.json"

FORCE_UPDATE = True

systems = dict()
commodities = dict()
listings = dict()


def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))


def download(url, path):
    if not path.exists() or FORCE_UPDATE:
        print("Downloading {} data".format(path.name.split()[0]))
        urlretrieve(url, path, reporthook)
    data = []
    print("Reading {}".format(path.name))
    with open(path, "r", encoding="utf8") as read_file:
        if path.name.endswith(".csv"):
            data = list(csv.DictReader(read_file))
        elif path.name.endswith(".json"):
            data = json.load(read_file)
    return data


cache = ROOT.joinpath("cache")
if cache.exists():
    if not cache.is_dir():
        print("Could not create cache directory")
        exit(1)
else:
    cache.mkdir()

pickles = ROOT.joinpath("pickles")
if pickles.exists():
    if not pickles.is_dir():
        print("Could not create pickles directory")
        exit(1)
else:
    pickles.mkdir()

listings_pickle = pickles.joinpath("listings")
if listings_pickle.exists() and not FORCE_UPDATE:
    listings_data = pickle.load(open(listings_pickle, "rb"))
else:
    listings_path = cache.joinpath("listings.csv")
    listings_data = download(LISTINGS_URL, listings_path)
    pickle.dump(listings_data, open(listings_pickle, "wb"))

stations_pickle = pickles.joinpath("stations")
if stations_pickle.exists() and not FORCE_UPDATE:
    stations_data = pickle.load(open(stations_pickle, "rb"))
else:
    stations_path = cache.joinpath("stations.json")
    stations_data = download(STATIONS_URL, stations_path)
    pickle.dump(stations_data, open(stations_pickle, "wb"))

commodities_pickle = pickles.joinpath("commodities")
if commodities_pickle.exists() and not FORCE_UPDATE:
    commodities_data = pickle.load(open(commodities_pickle, "rb"))
else:
    commodities_path = cache.joinpath("commodities.json")
    commodities_data = download(COMMODITIES_URL, commodities_path)
    pickle.dump(commodities_data, open(commodities_pickle, "wb"))


populated_systems_pickle = pickles.joinpath("populated_systems")
if populated_systems_pickle.exists() and not FORCE_UPDATE:
    populated_systems_data = pickle.load(open(populated_systems_pickle, "rb"))
else:
    populated_systems_path = cache.joinpath("systems_populated.json")
    populated_systems_data = download(
        POPULATED_SYSTEMS_URL, populated_systems_path)
    pickle.dump(populated_systems_data, open(populated_systems_pickle, "wb"))

listings = pd.DataFrame(listings_data)
stations = pd.DataFrame(stations_data)
commodities = pd.DataFrame(commodities_data)
populated_systems = pd.DataFrame(populated_systems_data)

mgf_listings = listings[listings.commodity_id == "304"]

mgf_listings.sell_price = mgf_listings.sell_price.astype(int)
mgf_listings.buy_price = mgf_listings.buy_price.astype(int)

sell_listings = mgf_listings.sort_values(
    by="sell_price", ascending=False).head(10)
buy_listings = mgf_listings.sort_values(by="buy_price", ascending=False)

sell_stations = stations.loc[stations["id"].isin(sell_listings.station_id)]
buy_stations = stations.loc[stations["id"].isin(buy_listings.station_id)]

sell_systems = populated_systems.loc[populated_systems["id"].isin(sell_stations.system_id)]
buy_systems = populated_systems.loc[populated_systems["id"].isin(buy_stations.system_id)]

print(sell_systems)