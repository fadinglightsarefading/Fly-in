import os
import sys
from pathlib import Path
from time import sleep
from models import Hub, Connection, Map


def choose_map() -> str:
    maps_dir = Path(__file__).parent / "maps"
    txt_files = list(maps_dir.rglob("*.txt"))
    while True:
        os.system("clear")
        print("   === Map selection ===")
        for i, file in enumerate(txt_files, start=1):
            print(f"   {i}.\t{file.name}")
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


def init_hubs(hub_configs: list[str], nb_drones: int) -> list[Hub]:
    if hub_configs.count("start_hub") >=2 or hub_configs("end_hub") >= 2:
        raise ValueError("'start_hub' or 'end_hub' appear more than once")

    hubs: list[Hub] = []
    for line in hub_configs:
        metadata = []
        if '[' in line and ']' in line:
            line = line.replace(" [", '&').replace(']', '')
            config_ln, _, metadata_ln = line.partition('&')
            config = config_ln.split()
            metadata = metadata_ln.split()
            if len(config) > 4 or len(metadata) > 3:
                raise ValueError("extra information present in hub configurations")
        else:
            config = line.split()
            if len(config) > 4:
                raise ValueError("extra information present in hub configurations")
        try:
            hubs.append(Hub(
                name=config[1],
                x=int(config[2]),
                y=int(config[3]),
            ))
        except ValueError:
            raise ValueError("invalid coordinate configuration")

        if "start_hub:" in config or "end_hub:" in config:
            if "start_hub:" in config:
                hubs[-1].zone="start"
            elif "end_hub:" in config:
                hubs[-1].zone="end"
            if metadata:
                for attribute in metadata:
                    if "color=" in attribute:
                        hubs[-1].color=attribute.replace("color=", '')
        elif "hub:" in congif:
            if metadata:
                for attribute in metadata:
                    if "zone=" in attribute:
                        hubs[-1].zone=attribute.replace("zone=", '')
                    elif "color=" in attribute:
                        hubs[-1].color=attribute.replace("color=", '')
                    elif "max_drones=" in attribute:
                        try:
                            hubs[-1].max_drones=int(attribute.replace("max_drones", ''))
                        except ValueError:
                            raise ValueError("invalid max_drones configuration")
        print(f"Name: {hubs[-1].name}\nX: {hubs[-1].x}\nY: {hubs[-1].y}\ni"
               "{hubs[-1].{hubs[-1].{hubs[-1].")
               # DO THIS - FINISHED HERE!

    return hubs



def parsing() -> None:
    map_config = choose_map()
    hub_configs: list[str] = []
    connection_configs: list[str] = []
    for line in map_config:
        if not line.strip() or line.lstrip().startswith('#'):
            continue
            line = line.replace('[', '').replace(']', '')
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

    hubs = init_hubs(hub_configs, nb_drones)
    #connections = init_connections(connection_configs)
