#! /usr/bin/bash

echo "Deprecated."

# docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
#   -i /local/ue_dataset_api.yaml \
#   -g python \
#   -o /local/genfiles \
#   --global-property models

# # Move genfiles/openapi-client/models to ./../models
# mv genfiles/openapi-client/models ./../models

# TODO Manually
# - Edit import path 
# - Remove `models_validate`