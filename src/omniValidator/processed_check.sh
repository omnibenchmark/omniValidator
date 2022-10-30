#!/usr/bin/env bash

###################################
# Processed data check
# validates normalized counts, dimension reduction and HVG.
# meant to be run by the `process_*.sh` script of processed data modules. 
###################################

function schema_check_processed () {( set -e
  
  #1: dataset_name
  #2: TAG_LIST
  
  local dataset_name=$1
  shift
  local TAG_LIST=$@
  
  for TAG in ${TAG_LIST[@]}
     do
        echo -n "checking files against JSON schema for tag $TAG ..."
        jsonschema src/utils/checks/$TAG/hvg_schema.json \
            -i data/$TAG/hvg_$dataset_name.json \
            -F "ERROR: {error.path} {error.message} \ "
            
        echo -n "checking norm counts and dim red mtx files ..."
        gunzip -c data/$TAG/norm_counts_$dataset_name.mtx.gz > data/$TAG/norm_counts_$dataset_name.mtx
        gunzip -c data/$TAG/dim_red_$dataset_name.mtx.gz > data/$TAG/dim_red_$dataset_name.mtx
        ncells_norm=`head -2 data/$TAG/norm_counts_$dataset_name.mtx | tail -1 | awk '//{print $2}' `
        ncells_dimred=`head -2 data/$TAG/dim_red_$dataset_name.mtx | tail -1 | awk '//{print $1}' `
        ngenes_norm=`head -2 data/$TAG/norm_counts_$dataset_name.mtx | tail -1 | awk '//{print $1}' `
        ncells_datainfo=`jq '.n_cells' data/$dataset_name/data_info_$dataset_name.json |  tr -d '[]"'`
        ngenes_datainfo=`jq '.n_genes' data/$dataset_name/data_info_$dataset_name.json |  tr -d '[]"'`

        if [ "$ncells_norm" -ne "$ncells_dimred" ]
            then 
            echo "Error: number of cells in dim_red and norm_counts don't match"
            exit 1
        fi

        if [ "$ncells_norm" -ne "$ncells_datainfo" ]
            then 
            echo "Error: number of cells in dim_red and norm_counts don't match"
            exit 1
        fi

        if [ "$ngenes_norm" -ne "$ngenes_datainfo" ]
            then 
            echo "Error: number of cells in dim_red and norm_counts don't match"
            exit 1
        fi

        rm data/$TAG/dim_red_$dataset_name.mtx
        rm data/$TAG/norm_counts_$dataset_name.mtx
        
        echo "OK!"
            
    done
)}
