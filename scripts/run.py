#! /usr/bin/python3.12

RAND_SEED = 163
DATA_SET_FILE = "testcase/sample.json"

from models import dataset


def __main__():
    # read file from json
    with open(DATA_SET_FILE, "r") as f:
        rawdata = f.read()
        f.close()

    # create dataset object
    data = dataset.Dataset()
    data.from_json(rawdata)

    print(f"Using Dataset: {data.Name}")

    # Application Map
    app_map = {}
    for app in data.Application:
        app_map[app.Id] = app


if __name__ == "__main__":
    __main__()
