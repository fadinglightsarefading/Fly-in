import sys
from parsing import parsing
from models import Hub, Connection, Map


def main() -> None:
    try:
        map = parsing()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"nb_drones: {map.number_of_drones}\n")
    print(f"{map.start_hub.zone}: {map.start_hub.name} {map.start_hub.x} "
          f"{map.start_hub.y} {map.start_hub.color} {map.start_hub.max_drones}")
    for hub in map.hubs:
        print(f"{hub.zone}: {hub.name} {hub.x} {hub.y} {hub.color} {hub.max_drones}")
    print(f"{map.end_hub.zone}: {map.end_hub.name} {map.end_hub.x} "
          f"{map.end_hub.y} {map.end_hub.color} {map.end_hub.max_drones}\n")
    for connection in map.connections:
        print(f"{connection.source}-{connection.destination} [{connection.max_link_capacity}]")
    print()


if __name__ == "__main__":
    main()
