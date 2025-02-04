# AppInterval


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**app_id** | **int** |  | [optional] 
**start_time** | **float** | Start time of the application | [optional] 
**end_time** | **float** | End time of the application | [optional] 

## Example

```python
from openapi_client.models.app_interval import AppInterval

# TODO update the JSON string below
json = "{}"
# create an instance of AppInterval from a JSON string
app_interval_instance = AppInterval.from_json(json)
# print the JSON string representation of the object
print(AppInterval.to_json())

# convert the object into a dict
app_interval_dict = app_interval_instance.to_dict()
# create an instance of AppInterval from a dict
app_interval_from_dict = AppInterval.from_dict(app_interval_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


