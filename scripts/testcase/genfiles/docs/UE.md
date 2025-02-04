# UE


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Unique identifier for the UE | [optional] 
**imsi** | **str** | IMSI for the UE | [optional] 
**arrival_time** | **float** | Time when the UE arrives in the network | [optional] 
**applications** | [**List[AppInterval]**](AppInterval.md) | List of applications with start and end times | [optional] 
**leave_time** | **float** | Time when the UE leaves the network | [optional] 

## Example

```python
from openapi_client.models.ue import UE

# TODO update the JSON string below
json = "{}"
# create an instance of UE from a JSON string
ue_instance = UE.from_json(json)
# print the JSON string representation of the object
print(UE.to_json())

# convert the object into a dict
ue_dict = ue_instance.to_dict()
# create an instance of UE from a dict
ue_from_dict = UE.from_dict(ue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


