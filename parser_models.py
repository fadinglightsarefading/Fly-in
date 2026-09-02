from pydantic import ValidationError
from models import Hub, Connection


class HubParser:
    def __init__(self, nb_drones: int):
        self.nb_drones = nb_drones
        self.hubs: list[Hub] = []
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None

    def init_hubs(self, hub_configs: list[str]) -> None:
        for line in hub_configs:
            config, metadata = self.parse_config(line)
            for hub in self.hubs:
                if hub.name == config[1]:
                    raise ValueError("duplicate hub names")
            try:
                if "start_hub:" in config or "end_hub:" in config:
                    self.special_hubs(config, metadata)
                elif "hub:" in config:
                    self.regular_hubs(config, metadata)
            except ValidationError as e:
                raise ValueError(e.errors()[0]["msg"])

    def special_hubs(self, config: list[str], metadata: list[str]) -> None:
        try:
            x = int(config[2])
            y = int(config[3])
        except ValueError:
            raise ValueError("invalid coordiante configuration")
        if "start_hub:" in config:
            self.start_hub = Hub(
                name=config[1],
                x=x,
                y=y,
                max_drones=self.nb_drones
            )
            for attribute in metadata:
                if "color=" in attribute:
                    self.start_hub.color=attribute.replace("color=", '')
        elif "end_hub:" in config:
            self.end_hub = Hub(
                name=config[1],
                x=x,
                y=y,
                max_drones=self.nb_drones
            )
            for attribute in metadata:
                if "color=" in attribute:
                    self.end_hub.color=attribute.replace("color=", '')

    def regular_hubs(self, config: list[str], metadata: list[str]) -> None:
        try:
            x = int(config[2])
            y = int(config[3])
        except ValueError:
            raise ValueError("invalid coordinate configuration")
        self.hubs.append(Hub(
            name=config[1],
            x=x,
            y=y,
        ))
        for attribute in metadata:
            if "zone=" in attribute:
                self.hubs[-1].zone=attribute.replace("zone=", '')
            elif "color=" in attribute:
                self.hubs[-1].color=attribute.replace("color=", '')
            elif "max_drones=" in attribute:
                try:
                    self.hubs[-1].max_drones=int(attribute.replace("max_drones=", ''))
                except ValueError:
                    raise ValueError("invalid max_drones configuration")

    def parse_config(self, line: str) -> tuple[list[str], list[str]]:
        metadata: list[str] = []
        if '[' in line and ']' in line:
            if '=' not in line:
                raise ValueError("metadata configuration invalid")
            line = line.replace(" [", '&').replace(']', '')
            config_ln, _, metadata_ln = line.partition('&')
            if (
                    metadata_ln.count("zone=") >= 2 or
                    metadata_ln.count("color=") >= 2 or
                    metadata_ln.count("max_drones=") >= 2
            ):
                raise ValueError("attribute duplicate present in metadata")
            config = config_ln.split()
            metadata = metadata_ln.split()
            if len(config) > 4 or len(metadata) > 3:
                raise ValueError("extra information present in hub configurations")
            for attribute in metadata:
                if (
                            "zone=" not in attribute and
                            "color=" not in attribute and
                            "max_drones=" not in attribute
                ):
                    raise ValueError("metadata configuration invalid")
        elif (('[' in line and ']' not in line) or ('[' not in line and ']' in line) or
              (
                  ("zone=" in line or "color=" in line or "max_drones" in line)
                  and ('[' not in line and ']' not in line)
        )):
            raise ValueError("metadata configuration invalid")
        else:
            config = line.split()
            if len(config) > 4:
                raise ValueError("extra information present in hub configurations")
        return config, metadata


class ConnectionParser:
    def __init__(self):
        self.connections: list[Connection] = []

    def init_connections(self, connection_configs: list[str]) -> None:
        for line in connection_configs:
            line = line.split(' ')
            if '-' not in line[1]:
                raise ValueError("missing hyphen in connection configuration") # test
            if len(line) == 2:
                connection = line[1].split('-')
                self.connections.append(Connection(
                    source=connection[0],
                    destination=connection[1],
                ))
            elif len(line) == 3:
                self.with_metadata(line)
            else:
                raise ValueError("connection metadata invalid") # test
        
    def with_metadata(self, line: list[str]) -> None:
        if (
                ('[' not in line[2] or ']' not in line[2])
                or ("max_link_capacity=" not in line[2])
        ):
            raise ValueError("invalid connection metadata configuraiton")
        connection = line[1].split('-')
        source = connection[0]
        destination = connection[1]
        try:
            max_cap = int(line[2].replace("[max_link_capacity=", '').replace(']', ''))
        except ValueError:
            raise ValueError("invalid connection metadata configuration")
        self.connections.append(Connection(
            source=source,
            destination=destination,
            max_link_capacity=max_cap
        ))
