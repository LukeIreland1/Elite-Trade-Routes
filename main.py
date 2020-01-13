import csv
import json
import sys
import urllib.request
from pathlib import Path
from urllib.request import urlretrieve

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
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

def download(url, path):
    if not path.exists():
        print("Getting {} data".format(path.name.split()[0]))
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

listings_path = cache.joinpath("listings.csv")
listings_data = download(LISTINGS_URL, listings_path)

stations_path = cache.joinpath("stations.json")
stations_data = download(stations_URL, stations_path)

commodities_path = cache.joinpath("commodities.json")
commodities_data = download(commodities_URL, commodities_path)

print(commodities_data)