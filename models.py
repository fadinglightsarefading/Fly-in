from pydantic import BaseModel, Field, ConfigDict, model_validator, ValidationError


class Hub(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    name: str
    x: int
    y: int
    zone: str = Field(default="normal")
    color: str = Field(default="none")
    max_drones: int = Field(default=1, ge=1)

    @model_validator(mode="after")
    def hub_validator(self):
        if self.zone not in {"normal", "blocked", "restricted", "priority"}:
            raise ValueError("invalid zone type")
        if '-' in self.name:
            raise ValueError("hyphens not allowed in hub names")
        return self


class Connection(BaseModel):
    source: str
    destination: str
    max_link_capacity: int = Field(default=1, ge=1)


class Map(BaseModel):
    number_of_drones: int = Field(ge=1)
    hubs: list[Hub]
    connections: list[Connection]
    start_hub: Hub
    end_hub: Hub

    @model_validator(mode="after")
    def map_validator(self):
        hub_names = [hub.name for hub in self.hubs]
        hub_names.append(self.start_hub.name)
        hub_names.append(self.end_hub.name)
        self.validate_hubs(hub_names)
        self.validate_connections(hub_names)
        #   - no paths between hubs whose coordinates are merely one apart
        return self

    def validate_hubs(self, hub_names: list[str]) -> None:
        if len(hub_names) != len(set(hub_names)):
            raise ValueError("duplicate hub names")
        hub_coords = [
            tuple(sorted((hub.x, hub.y)))
            for hub in self.hubs
        ]
        hub_coords.append(tuple(sorted((self.start_hub.x, self.start_hub.y))))
        hub_coords.append(tuple(sorted((self.end_hub.x, self.end_hub.y))))
        if len(hub_coords) != len(set(hub_coords)):
            raise ValueError("duplicate coordinates")

    def validate_connections(self, hub_names: list[str]) -> None:
        if not self.connections:
            raise ValueError("no connections present")
        for connection in self.connections:
            if connection.source not in hub_names or connection.destination not in hub_names:
                raise ValueError("connection linking a non-previously-defined zone")
        check_dupes = [
            tuple(sorted((connection.source, connection.destination)))
            for connection in self.connections
        ]
        if len(check_dupes) != len(set(check_dupes)):
            raise ValueError("duplicate connections")

