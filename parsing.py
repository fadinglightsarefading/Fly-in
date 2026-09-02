import os
import sys
from pathlib import Path
from time import sleep
from pydantic import ValidationError
from models import Hub, Connection, Map
from parser_models import HubParser, ConnectionParser


def choose_map() -> str:
    maps_dir = Path(__file__).parent / "maps"
    txt_files = list(maps_dir.rglob("*.txt"))
    while True:
        os.system("clear")
        print("   === Map selection ===")
        for i, file in enumerate(txt_files, start=1):
            print(f"   {i}.\t{file.name} ({file.parent.name})")
        print("   0.\tExit")
        print("\nChoose wisely: ", end='')
        try:
            choice = int(input())
            if 0 <= choice <= len(txt_files):
                break
            else:
                print("Error: input must be one of the above")
                sleep(2)
        except ValueError as e:
            print("Error: invalid input")
            sleep(2)
    if choice == 0:
        sys.exit(0)
    with open(txt_files[choice - 1], 'r') as map_config:
        return map_config.read().splitlines()


def partition_configs(map_config: list[str]) -> tuple[str, str, int]:
    # check for everything necessary being present, e.g. no missing nb_drones - in model_validator
    nb_drones: int = -1
    hub_configs: list[str] = []
    connection_configs: list[str] = []
    for line in map_config:
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if line.startswith("nb_drones: "):
            try:
                nb_drones = int(line.split(':')[1].strip())
            except ValueError:
                raise ValueError("map file includes an invalid 'nb_drones' configuration")
        elif (
                line.startswith("start_hub:") or
                line.startswith("end_hub:") or
                line.startswith("hub:")
        ):
            hub_configs.append(line)
        elif line.startswith("connection:"):
            connection_configs.append(line)
        else:
            raise ValueError("invalid line present in map file")
    if nb_drones == -1:
        raise ValueError("nb_drones configuration missing")
    return hub_configs, connection_configs, nb_drones


def parsing() -> Map:
    hubconf, connconf, nb_drones = partition_configs(choose_map())

    hub_parser = HubParser(nb_drones)
    hub_parser.init_hubs(hubconf)

    connection_parser = ConnectionParser()
    connection_parser.init_connections(connconf)

    try:
        simulation = Map(
            number_of_drones=nb_drones,
            hubs=hub_parser.hubs,
            connections=connection_parser.connections,
            start_hub=hub_parser.start_hub,
            end_hub=hub_parser.end_hub
        )
    except ValidationError as e:
        raise ValueError(e.errors()[0]["msg"])
    return simulation
