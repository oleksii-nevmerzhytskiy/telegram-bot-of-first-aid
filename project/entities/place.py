from dataclasses import dataclass


@dataclass
class Place:
    place_name: str = None
    place_address: str = None
    latitude: float = None
    longitude: float = None

