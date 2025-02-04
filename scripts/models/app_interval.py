from typing import Any, Dict, Optional
from typing_extensions import Self

# Sample data
# {
#     "Id": 0,
#     "start_time": 20.3,
#     "end_time": 40.3
# }


class AppInterval:

    def __init__(self, Id: int, start_time: float, end_time: float):
        self.Id = Id
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return (
            f"Id: {self.Id}, start_time: {self.start_time}, end_time: {self.end_time}"
        )

    def to_dict(self):
        return {"Id": self.Id, "start_time": self.start_time, "end_time": self.end_time}

    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None
        return cls(
            Id=obj.get("Id"),
            start_time=obj.get("start_time"),
            end_time=obj.get("end_time"),
        )
