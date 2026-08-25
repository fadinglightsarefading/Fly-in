from parsing import parsing
from models import Hub, Connection, Map


def main() -> None:
    try:
        parsing()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    hubs: list[Hub] = []
    hname = "corridorA"
    hx = 4
    hy = 3
    zone = "priority"
    color = "green"
    max_drones = 2

    hubs.append(
        Hub(
            name=hname,
            x=hx,
            y=hy,
        )
    )
    if zone:
        hubs[-1].zone = zone
    if color:
        hubs[-1].color = color
    if max_drones:
        hubs[-1].max_drones = max_drones


if __name__ == "__main__":
    main()
