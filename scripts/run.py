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

    print("Dataset:", data)

    print("Dict:\n", data.to_dict())


if __name__ == "__main__":
    __main__()
