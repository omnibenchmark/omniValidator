#!/usr/bin/env bash

###################################
# Methods output check
# Validates reconstructed dimension reduction
# Meant to be run by the `process_*.sh` script of methods modules. 
# Will loop thourhg detected datasets that have a meta_ file. 
# Eg use. `check_methods $OMNI_TYPE ${DATA_VARS['name']} ${METH}`
###################################

function check_methods () {( set -e
  
  #1: folder of processed data
  local INPUT=$1
  #2: folder of method output
  local OUT=$2
  #3: name of method
  local METH=$3

  DS=`ls data/$INPUT | grep '^meta_.*.json'` 
  DS=`for i in ${DS[@]}; do echo ${i#"meta_"}; done`
  DS=`for i in ${DS[@]}; do echo ${i%".json"}; done`

  for DATASET in ${DS[@]}
    do


        ALL_DIMRED_REC=`ls data/$OUT | grep "^${METH}_${DATASET}.*red_dim.mtx.gz$"`
        for DIMRED_REC in ${ALL_DIMRED_REC[@]}
            do
                printf "Checking file ${DIMRED_REC}..."
                gunzip -c data/$OUT/$DIMRED_REC > data/$OUT/${DIMRED_REC%.gz}
                gunzip -c data/$INPUT/dim_red_${DATASET}.mtx.gz > data/$INPUT/dim_red_${DATASET}.mtx
                gunzip -c data/$INPUT/norm_counts_${DATASET}.mtx.gz > data/$INPUT/norm_counts_${DATASET}.mtx
                NCELLS_DIMRED_REC=`head -2 data/$OUT/${DIMRED_REC%.gz} | tail -1 | awk '//{print $1}' `
                NCELLS_DIMRED=`head -2 data/$INPUT/dim_red_${DATASET}.mtx | tail -1 | awk '//{print $1}' `
                NCELLS_NORM=`head -2 data/$INPUT/norm_counts_${DATASET}.mtx | tail -1 | awk '//{print $2}' `


                if [ "$NCELLS_DIMRED_REC" -ne "$NCELLS_DIMRED" ]
                    then 
                    echo "Error: number of cells in dim_red and reconstructed dim_red don't match for file ${DIMRED_REC}"
                    exit 1
                fi

                if [ "$NCELLS_NORM" -ne "$NCELLS_DIMRED_REC" ]
                    then 
                    echo "Error: number of cells in reconstructed dim_red and norm_counts don't match for file ${DIMRED_REC}"
                    exit 1
                fi

                rm data/$OUT/${DIMRED_REC%.gz}
                rm data/$INPUT/dim_red_${DATASET}.mtx
                rm data/$INPUT/norm_counts_${DATASET}.mtx
                printf "OK\n"
            done

    done
  
)}
