#!/bin/bash

DATASET_NAME='lipid_bilayer_vesicles'
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATASET_PATH="$(realpath "$SCRIPT_DIR/../../..")"/

# Get Sampler for all labelled data
python data_generator/default/GeneratorSampler.py \
    --data-root $DATASET_PATH \
    --data-folder $DATASET_NAME/ \
    --dataset-id $DATASET_NAME 