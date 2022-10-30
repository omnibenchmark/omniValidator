#!/usr/bin/env bash

###################################
# Metrics check
# validates the metrics json and the metric info json
# meant to be run by the `run_metric.sh` script of the metric modules. 
###################################

function schema_check_metric () {( set -e
    
    #1 OUT_PATH/dataset_name
    #2 TAG_LIST 
    local DS_PATH=$1
    local TAG=$2

    DS_FILES=`ls $DS_PATH`

    for DS_FILE in ${DS_FILES[@]}
        do
            DS=$DS_PATH/$DS_FILE
            printf "checking file $DS against JSON schema ..."

            if [[ "$DS" =~ ^${METRIC_NAME}_info ]]; then
              jsonschema src/utils/checks/$TAG/metric_info_schema.json \
                -i $DS \
                -F "ERROR: {error.path} {error.message} \ "
            else
                jsonschema src/utils/checks/$TAG/metric_schema.json \
                    -i $DS \
                    -F "ERROR: {error.path} {error.message} \ "
            fi 
            printf "OK\n"

        done
)}


