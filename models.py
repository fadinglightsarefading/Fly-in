from pydantic import BaseModel, Field, ConfigDict, model_validator, ValidationError


class Hub(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    name: str
    x: int
    y: int
    zone: str = Field(default="normal") # if zone = start or end, zone = start or end
    color: str = Field(default="none")
    max_drones: int = Field(default=1, ge=1) # if zone = start or end, max = nb_drones

    @model_validator(mode="after")
    def parser_constraints(self):
        if self.zone not in {"start", "end", "normal", "blocked", "restricted", "priority"}:
            raise ValueError("invalid zone type")
        return self


class Connection(BaseModel):
    source: str
    destination: str
    max_link_capacity: int = Field(default=1, ge=1)


class Map(BaseModel):
    number_of_drones: int = Field(ge=1)
    hubs: list[Hub]
    connections: list[Connections]
    start_hub: Hub
    end_hub: Hub

    # model_validator:
    #   - each zone must have a unique name and valid int coordinates
    #   - connections must link only previously defined zones using
    #     connection: <zone1>-<zone2> [metadata]
    #   - the same connection must not apprear more than once (a-b b-a duplicates)
