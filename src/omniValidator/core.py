import json
import os as os
from jsonschema import validate
import jsonref
import jsonschema # <--
import logging
from os.path import dirname
import re
import warnings

## TODO: check if everything is used 


def read_json_file(file_path):
    """
    Reads the file at the file_path and returns the contents.
        Returns:
            json_content: Contents of the json file

    """
    try:
        json_content_file = open(file_path, 'r')
    except IOError as error:
        print(error)

    else:
        try:
            base_path = dirname(file_path)
            base_uri = 'file://{}/'.format(base_path)
            json_schema = jsonref.load(json_content_file, base_uri=base_uri, jsonschema=True)
        except (ValueError, KeyError) as error:
            print(file_path)
            print(error)

        json_content_file.close()

    return json_schema


def get_schema(benchmark, keyword, ftype): 
    """
    Returns the schema file path. Schemas are stored in the `schemas` folder of the package. 

    Args: 
        benchmark: omnibenchmark name. 
        keyword: keyword associated to the project (i.e., keyword specific to 'data', 'method', etc)
        ftype: file type name. 
    """
    from omniValidator import __path__ as omni_val_path     
    schema_path = os.path.join(omni_val_path[0], 'schemas', benchmark, keyword, ftype+'.json')
    return(schema_path)


def validate_json_file(json_input_path, json_schema_path):
    """
    Validates a JSON file based on a schema file. Paths to module's schemas can be obtained with `get_schema`.

    Args: 
        json_input_path: input path to test against the schema
        json_schema_path: path to the schema file

    Returns: 
        boolean, with error message if invalid. 

    """
    req_schema = read_json_file(json_schema_path)
    json_data = read_json_file(json_input_path)
    #print("SCHEMA --> "+str(req_schema))
    try:
        validate(instance=json_data, schema=req_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return False, err

    message = "Given JSON data is Valid"
    return True, message





def validate_requirements(benchmark, keyword, data_folder):
    """
    Validates the outputs of an Omnibenchmark project. 

    Args: 
        benchmark (str):  benchmark name
        keyword (str): keyword that defines the current step of the benchmark 
        data_folder (str): path to the output files that need to be validated

    Returns: 
        Error, 


    """
    from omniValidator import __path__ as omni_val_path     

    ## Loads requir file
    requir = os.path.join(omni_val_path[0], 'schemas', benchmark, keyword, 'output',  'requirements.json')
    f = open(requir)
    requir = json.load(f)

    ## Parse requirements into regex
    requir_names = list(requir['required'].keys())
    requir_end = [requir['required'][sub]['end'] for sub in requir['required']]
    regx = [a_ + ".*" + b_ for a_, b_ in zip(requir_names, requir_end)] 

    ## Validation
    listdir = os.listdir(data_folder)
    import re
    r = re.compile('.*(%s).*'%regx)
    newlist = list(filter(r.match, listdir)) 
    rcompiled = [re.compile('.*(%s).*'%reg) for reg in regx]
    files_found = [list(filter(rcomp.match, listdir)) for rcomp in rcompiled]
    print("Output files detected:")
    print(files_found)
    for i in range(len(files_found)): 
        if len(files_found[i]) == 0:
            msg = "no files associated to "+ regx[i]
            print(msg)
            break
        elif len(files_found[i]) > 1: 
            msg = "Multiple files associated to "+ regx[i] +":\n"+str(files_found[i])
            warnings.warn(msg)
        else: 
            print("Congrats! All outputs meet the requirements of the current stage. ")


