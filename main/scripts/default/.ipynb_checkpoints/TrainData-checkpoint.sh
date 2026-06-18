#!/bin/bash

DATASET_NAME='lipid_bilayer_vesicles'
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATASET_PATH="$(realpath "$SCRIPT_DIR/../../..")"/

# Get Sampler for all labelled data
python data_generator/default/GeneratorSampler.py \
    --data-root $DATASET_PATH \
    --data-folder $DATASET_NAME/ \
    --dataset-id $DATASET_NAME \
    --global-config config/default/global_parameters.yaml

# Training Data
python data_generator/default/GeneratorMask.py \
    --save-path synthetic_data/$DATASET_NAME/ \
    --N 3 \
    --dataset-id $DATASET_NAME \
    --config config/default/synth_parameters.yaml \
    --global-config config/default/global_parameters.yaml

# Baseline
python data_generator/default/GeneratorImage.py \
    --dataset-id $DATASET_NAME \
    --mask-dir synthetic_data/$DATASET_NAME/ \
    --sampler-dir data_$DATASET_NAME/ \
    --sub-folder base_texture/ \
    --config config/default/synth_parameters.yaml \
    --global-config config/default/global_parameters.yaml

# Speckling
python data_generator/default/GeneratorImage.py \
    --dataset-id $DATASET_NAME \
    --mask-dir synthetic_data/$DATASET_NAME/ \
    --sampler-dir data_$DATASET_NAME/ \
    --sub-folder speckling_texture/ \
    --config config/default/synth_parameters_speckling.yaml \
    --global-config config/default/global_parameters.yaml
    
# Width Scaling
python data_generator/default/GeneratorImage.py \
    --dataset-id $DATASET_NAME \
    --mask-dir synthetic_data/$DATASET_NAME/ \
    --sampler-dir data_$DATASET_NAME/ \
    --sub-folder width_scaling_texture/ \
    --config config/default/synth_parameters_width_scaling.yaml \
    --global-config config/default/global_parameters.yaml
    
# Speckling + Width Scaling
python data_generator/default/GeneratorImage.py \
    --dataset-id $DATASET_NAME \
    --mask-dir synthetic_data/$DATASET_NAME/ \
    --sampler-dir data_$DATASET_NAME/ \
    --sub-folder combined_texture/ \
    --config config/default/synth_parameters_combined.yaml \
    --global-config config/default/global_parameters.yaml

python plot.py