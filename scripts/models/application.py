from typing import Any, Dict, Optional
from typing_extensions import Self

# Sample data
# Application
# {
#     "Id": 0,
#     "Description": "Sample Application",
#     "MaxBR": "10M",
#     "MinBR": "1M"
# },


class Application:

    def __init__(self, Id: int, Description: str, MaxBR: str, MinBR: str):
        self.Id = Id
        self.Description = Description
        self.MaxBR = MaxBR
        self.MinBR = MinBR

    def __str__(self):
        return f"Id: {self.Id}, Description: {self.Description}, MaxBR: {self.MaxBR}, MinBR: {self.MinBR}"

    def to_dict(self):
        return {
            "Id": self.Id,
            "Description": self.Description,
            "MaxBR": self.MaxBR,
            "MinBR": self.MinBR,
        }

    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None
        return cls(
            Id=obj.get("Id"),
            Description=obj.get("Description"),
            MaxBR=obj.get("MaxBR"),
            MinBR=obj.get("MinBR"),
        )
