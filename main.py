import urllib.request
import json
import csv
from pathlib import Path

ROOT = Path(__file__).parent

SYSTEMS_URL = "https://eddb.io/archive/v6/systems.csv"
UPDATED_SYSTEMS_URL = "https://eddb.io/archive/v6/systems_recently.csv"
POPULATED_SYSTEMS_URL = "https://eddb.io/archive/v6/systems_populated.json"
BODIES_URL = "https://eddb.io/archive/v6/bodies.jsonl"
UPDATED_BODIES_URL = "https://eddb.io/archive/v6/bodies_recently.jsonl"
STATIONS_URL = "https://eddb.io/archive/v6/stations.json" 
FACTIONS_URL = "https://eddb.io/archive/v6/factions.json"
PRICES_URL = "https://eddb.io/archive/v6/listings.csv"
COMMODITIES_URL = "https://eddb.io/archive/v6/commodities.json"
MODULES_URL = "https://eddb.io/archive/v6/modules.json"

cache = ROOT.joinpath("cache")
if cache.exists():
    if not cache.is_dir():
        print("Could not create cache directory")
        exit(1)
else:
    cache.mkdir()

systems_path = cache.joinpath("systems.csv")
if not systems_path.exists():
    print("Getting systems data")
    urllib.request.urlretrieve(SYSTEMS_URL, systems_path)

with open(systems_path, "r", encoding="utf8") as read_file:
    systems_data = csv.DictReader(read_file)




commodities_path = cache.joinpath("commodities.csv")
if not commodities_path.exists():
    print("Getting commodities data")
    urllib.request.urlretrieve(COMMODITIES_URL, commodities_path)

with open(commodities_path, "r", encoding="utf8") as read_file:
    commodities_data = json.load(read_file)

print(systems_data, commodities_data)