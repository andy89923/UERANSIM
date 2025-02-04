from typing import Any, Dict, Optional, List
from typing_extensions import Self
import json

# Sample data
# {
#     "Name": "Sample Dataset",
#     "Application": [
#         {
#             "Id": 0,
#             "Description": "Sample Application",
#             "MaxBR": "10M",
#             "MinBR": "1M"
#         }
#     ],
#     "UE": [
#         {
#             "Id": 0,
#             "IMSI": "imsi-208930000008888",
#             "Arrival_Time": 16.3,
#             "Leave_Time": 50.3,
#             "Applications": [
#                 {
#                     "Id": 0,
#                     "start_time": 20.3,
#                     "end_time": 40.3
#                 }
#             ]
#         }
#     ]
# }

from models.application import Application
from models.ue import UserEquipment


class Dataset:

    def __init__(
        self,
        Name: str = "NOT_SET",
        Application: List[Application] = None,
        UE: List[UserEquipment] = None,
    ):
        self.Name = Name
        self.Application = Application
        self.UE = UE

    def __str__(self):
        return f"Name: {self.Name}, Application: {self.Application}, UE: {self.UE}"

    def to_dict(self):
        return {
            "Name": self.Name,
            "Application": [app.to_dict() for app in self.Application],
            "UE": [ue.to_dict() for ue in self.UE],
        }

    def from_dict(self, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        if obj is None:
            return None

        self.Name = obj.get("Name")
        self.Application = [
            Application.from_dict(Application, app) for app in obj.get("Application")
        ]
        self.UE = [UserEquipment.from_dict(UserEquipment, ue) for ue in obj.get("UE")]
        return self

    def from_json(self, json_str: str):
        obj = json.loads(json_str)
        return self.from_dict(obj)
