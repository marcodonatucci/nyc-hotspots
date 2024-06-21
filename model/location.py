from dataclasses import dataclass


@dataclass
class Location:
    Location: str
    Latitude: float
    Longitude: float

    def __hash__(self):
        return hash(self.Location)

    def __str__(self):
        return self.Location
