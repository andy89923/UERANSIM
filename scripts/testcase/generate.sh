#! /usr/bin/bash

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
  -i /local/ue_dataset_api.yaml \
  -g python \
  -o /local/genfiles \
  --global-property models