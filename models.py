from pydantic import BaseModel, Field

class Hub(BaseModel):
    name: str
    x: int
    y: int
    zone:str = Field(default="normal") # if zone = start or end, zone = start or end
    color:str = Field(default="none")
    max_drones:int = Field(default=1, ge=1) # if zone = start or end, max = nb_drones


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
