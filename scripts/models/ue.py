from typing import Any, Dict, Optional, List
from typing_extensions import Self

# Sample data
# "UE":
# {
#     "Id": 0,
#     "IMSI": "imsi-208930000008888",
#     "Arrival_Time": 16.3,
#     "Leave_Time": 50.3,
#     "Applications": [
#         {
#             "Id": 0,
#             "start_time": 20.3,
#             "end_time": 40.3
#         }
#     ]
# }

from models.app_interval import AppInterval


class UserEquipment:

    def __init__(
        self,
        Id: int,
        IMSI: str,
        Arrival_Time: float = 0.0,
        Leave_Time: float = 0.0,
        AppInterval: List[AppInterval] = [],
    ):
        self.Id = Id
        self.IMSI = IMSI
        self.Arrival_Time = Arrival_Time
        self.Leave_Time = Leave_Time
        self.AppInterval = AppInterval

    def __str__(self):
        return f"Id: {self.Id}, IMSI: {self.IMSI}, Arrival_Time: {self.Arrival_Time}, Leave_Time: {self.Leave_Time}, AppInterval: {self.Applications}"

    def to_dict(self):
        return {
            "Id": self.Id,
            "IMSI": self.IMSI,
            "Arrival_Time": self.Arrival_Time,
            "Leave_Time": self.Leave_Time,
            "AppInterval": [app.to_dict() for app in self.AppInterval],
        }

    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None
        return cls(
            Id=obj.get("Id"),
            IMSI=obj.get("IMSI"),
            Arrival_Time=obj.get("Arrival_Time"),
            Leave_Time=obj.get("Leave_Time"),
            AppInterval=[
                AppInterval.from_dict(AppInterval, app)
                for app in obj.get("AppInterval")
            ],
        )
