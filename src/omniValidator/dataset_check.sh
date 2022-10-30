#!/usr/bin/env bash

###################################
# Dataset check
# validates data info, meta info and features info based on the JSON schema validator
# meant to be run by the `load_dataset.sh` script of data modules. 
# Should automatically fetch the schemas needed for each omnibenchmark (TAG). 
###################################

function schema_check_dataset () {( set -e
  
  #1: dataset_name
  #2: TAG_LIST
  
  local dataset_name=$1
  shift
  local TAG_LIST=$@
  
  for TAG in ${TAG_LIST[@]}
     do
        echo -n "checking files against JSON schema for tag $TAG ..."
        jsonschema src/utils/checks/$TAG/data_info_schema.json \
            -i data/$dataset_name/data_info_$dataset_name.json \
            -F "ERROR: {error.path} {error.message} \ "

        jsonschema src/utils/checks/$TAG/feature_schema.json \
            -i data/$dataset_name/feature_$dataset_name.json \
            -F "ERROR: {error.path} {error.message} \ "

        jsonschema src/utils/checks/$TAG/meta_schema.json \
            -i data/$dataset_name/meta_$dataset_name.json \
            -F "ERROR: {error.path} {error.message} \ "

        echo "OK!"
            
    done
)}
