import os
import sys
from pathlib import Path
from time import sleep
from pydantic import ValidationError
from models import Hub, Connection, Map
from hub_parser import HubParser


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


def parsing() -> None:
    map_config = choose_map()
    hub_configs: list[str] = []
    connection_configs: list[str] = []
    # check for everything necessary being present, e.g. no missing nb_drones
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

    hub_parser = HubParser(nb_drones)
    hub_parser.init_hubs(hub_configs)
    print(f"\nNumber of drones: {nb_drones}") # delete
    for hub in hub_parser.hubs:
        print(f"\nName: {hub.name}\nX: {hub.x}\nY: {hub.y}\n"
              f"Zone: {hub.zone}\nColor: {hub.color}\nMax drones: {hub.max_drones}")
    #hubs = init_hubs(hub_configs, nb_drones)
    #connections = init_connections(connection_configs)
