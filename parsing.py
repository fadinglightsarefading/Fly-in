import os
import sys
from pathlib import Path
from time import sleep
from pydantic import ValidationError
from models import Hub, Connection, Map


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


def init_hubs(hub_configs: list[str], nb_drones: int) -> list[Hub]:
    if hub_configs.count("start_hub") >=2 or hub_configs.count("end_hub") >= 2:
        raise ValueError("'start_hub' or 'end_hub' appear more than once") # doesn't work
                                                                        # replace with thing in model
                                                                        # validator: duplicate names

    print(f"\nNumber of drones: {nb_drones}") # delete
    hubs: list[Hub] = []
    for line in hub_configs:
        metadata = []
        if '[' in line and ']' in line:
            if '=' not in line:
                raise ValueError("metadata configuration invalid")
            line = line.replace(" [", '&').replace(']', '')
            config_ln, _, metadata_ln = line.partition('&')
            config = config_ln.split()
            metadata = metadata_ln.split()
            if len(config) > 4 or len(metadata) > 3:
                raise ValueError("extra information present in hub configurations")
        elif (('[' in line and ']' not in line) or
              ('[' not in line and ']' in line) or
              (
                  ("zone=" in line or "color=" in line or "max_drones" in line)
                  and ('[' not in line and ']' not in line)
              )
        ):
            raise ValueError("metadata configuration invalid")
        else:
            config = line.split()
            if len(config) > 4:
                raise ValueError("extra information present in hub configurations")
        try:
            if metadata:
                for attribute in metadata:
                    if (
                            "zone=" not in attribute and
                            "color=" not in attribute and
                            "max_drones=" not in attribute # check if any of these present twice
                    ):
                        raise ValueError("metadata configuration invalid")
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
                try:
                    hubs[-1].max_drones=nb_drones
                except ValueError:
                    raise ValueError("invalid max_drones configuration")
                if metadata:
                    for attribute in metadata:
                        if "color=" in attribute:
                            hubs[-1].color=attribute.replace("color=", '')
            elif "hub:" in config:
                if metadata:
                    for attribute in metadata:
                        if "zone=" in attribute:
                            hubs[-1].zone=attribute.replace("zone=", '')
                        elif "color=" in attribute:
                            hubs[-1].color=attribute.replace("color=", '')
                        elif "max_drones=" in attribute:
                            try:
                                hubs[-1].max_drones=int(attribute.replace("max_drones=", ''))
                            except ValueError:
                                raise ValueError("invalid max_drones configuration")
        except ValidationError as e:
            raise ValueError(e.errors()[0]["msg"])
        print(f"\nName: {hubs[-1].name}\nX: {hubs[-1].x}\nY: {hubs[-1].y}\n"
              f"Zone: {hubs[-1].zone}\nColor: {hubs[-1].color}\nMax drones: {hubs[-1].max_drones}")

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
