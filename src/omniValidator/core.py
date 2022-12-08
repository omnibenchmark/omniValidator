import json
import os as os
from jsonschema import validate
import jsonref
import jsonschema # <--
#import logging
from os.path import dirname
import re
import warnings

class ValidationError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)


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
        boolean, with error message if invalid. If valid, returns True.

    """
    req_schema = read_json_file(json_schema_path)
    json_data = read_json_file(json_input_path)
    #print("SCHEMA --> "+str(req_schema))
    try:
        validate(instance=json_data, schema=req_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return err

    print("Given JSON data is valid!")
    return True



def validate_requirements(omni_obj=None, benchmark=None, keyword=None, data_folder=None):
    """
    Validates the outputs of an Omnibenchmark project from files or from an `omnibenchmark` object.

    If `omni_obj` is not specified, all other arguments should be provided. 

    Args: 
        omni_obj (omniObject): omni object from the omnibenchmark module
        benchmark (str):  benchmark name
        keyword (str): keyword that defines the current step of the benchmark 
        data_folder (str): path to the output files that need to be validated.

    Returns: 
        Raises an Exception error is an output file is missing. Else, returns True.


    """
    from omniValidator import __path__ as omni_val_path   

     # args requirements
    if omni_obj is None:
        if benchmark is None and keyword is None and data_folder is None: 
            msg = " if `omni_obj` is not specified, the other arguments are required."
            raise Exception(msg)
    if data_folder is not None and omni_obj is not None: 
        msg = "both `data_folder` and `omni_obj` are provided but only 1 required. Only `omni_obj` will be used."
        warnings.warn(msg)
    if omni_obj is not None: 
        if keyword is not None:
            msg = "both `omni_obj` and `keyword` are provided. Using `keyword` argument only."
            warnings.warn(msg)
        else: 
            if len(omni_obj.keyword) > 2: 
                msg = "multiple keywords found in the `omni_obj`. Using the first one."
                warnings.warn(msg)
            keyword = omni_obj.keyword[0]

        if benchmark is not None: 
            msg = "both `omni_obj` and `benchmark` are provided. Using `benchmark` argument only."
            warnings.warn(msg)
        else: 
            benchmark = omni_obj.benchmark_name        

    ## Loads requir file
    requir = os.path.join(omni_val_path[0], 'schemas', benchmark, keyword, 'output',  'requirements.json')
    f = open(requir)
    requir = json.load(f)

    ## Parse requirements into regex
    requir_names = list(requir['required'].keys())
    requir_end = [requir['required'][sub]['end'] for sub in requir['required']]
    regx = [a_ + ".*" + b_ for a_, b_ in zip(requir_names, requir_end)] 

    ## list
    if omni_obj is None: 
        data_folder = os.path.join(data_folder, '')
        listdir = os.listdir(data_folder)
    else: 
        listdir = [omni_obj.outputs.file_mapping[0]['output_files'][k] for k in omni_obj.outputs.file_mapping[0]['output_files'].keys()]

    ## regex and find
    r = re.compile('.*(%s).*'%regx)
    rcompiled = [re.compile('.*(%s).*'%reg) for reg in regx]
    files_found = [list(filter(rcomp.match, listdir)) for rcomp in rcompiled]
    subst =[[]]*len(requir_names)
    CNT = 0
    for i in requir_names: 
        try: 
            subst[CNT] = requir['required'][i]['substitutable_with']
            CNT = CNT +1
        except: 
            CNT = CNT +1
            continue

    print("Output files detected:")
    print(files_found)
    for i in range(len(files_found)): 
        if len(files_found[i]) == 0:

            # try to search among substitutes files
            if len(subst[i]) >0: 
                for j in range(len(subst[i])): 
                    # all substitutes tried, stop.
                    if len(files_found[requir_names.index(subst[i][j])]) > 0: 
                        print("Substitute found for", regx[i], ":", subst[i][j])
                    elif j == len(subst[i])-1:
                        msg = "no files associated to "+ regx[i]
                        print(msg)
                        raise Exception(msg)
            else: 
                msg = "no files associated to "+ regx[i]
                raise Exception(msg)

        elif len(files_found[i]) > 1: 
            msg = "Multiple files associated to "+ regx[i] +":\n"+str(files_found[i])
            warnings.warn(msg)
    print("\nValidated! All outputs meet the requirements of '", keyword, "'\n")
    return True


def validate_all(benchmark, keyword, data_folder): 
    """
    Simultaneous vadlidation of requirements and JSON files using the JSON schemas of Omnivalidator.
    
    Args: 
        benchmark (str): benchmark name
        keyword (str): keyword that defines the current step of the benchmark 
        data_folder (str): path to the output files that need to be validated

    Returns:
        Raises an Exception error is an output file is missing or a JSON badly formatted. Else, returns True.

    """
    from omniValidator import __path__ as omni_val_path     

    # args requirements
    if data_folder is None:
        msg = "`data_folder` or `omni_obj` are required."
        raise Exception(msg)
    if data_folder is not None: 
        msg = "both `data_folder` and `omni_obj` are provided but only 1 required. Only `omni_obj` will be used."
        warnings.warn(msg)
        
    ## Loads requir file
    requir = os.path.join(omni_val_path[0], 'schemas', benchmark, keyword, 'output',  'requirements.json')
    f = open(requir)
    requir = json.load(f)

    ## Parse requirements into regex
    requir_names = list(requir['required'].keys())
    requir_end = [requir['required'][sub]['end'] for sub in requir['required']]
    regx = [a_ + ".*" + b_ for a_, b_ in zip(requir_names, requir_end)] 
    requir_dict = dict(zip(requir_names, requir_end))

    ## compile files and schemas
    data_folder = os.path.join(data_folder, '')
    listdir = os.listdir(data_folder)
    import re
    r = re.compile('.*(%s).*'%regx)
    newlist = list(filter(r.match, listdir)) 
    rcompiled = [re.compile('.*(%s).*'%reg) for reg in regx]
    files_found = [list(filter(rcomp.match, listdir)) for rcomp in rcompiled]
    subst =[[]]*len(requir_names)
    CNT = 0
    for i in requir_names: 
        try: 
            subst[CNT] = requir['required'][i]['substitutable_with']
            CNT = CNT +1
        except: 
            CNT = CNT +1
            continue

    print("Output files detected:")
    print(files_found)
    for i in range(len(files_found)): 
        if len(files_found[i]) == 0:

            # try to search among substitutes files
            if len(subst[i]) >0: 
                for j in range(len(subst[i])): 
                    # all substitutes tried, stop.
                    if len(files_found[requir_names.index(subst[i][j])]) > 0: 
                        print("Substitute found for", regx[i], ":", subst[i][j])
                    elif j == len(subst[i])-1:
                        msg = "no files associated to "+ regx[i]
                        print(msg)
                        raise Exception(msg)
            else: 
                msg = "no files associated to "+ regx[i]
                raise Exception(msg)

        elif len(files_found[i]) > 1: 
            msg = "Multiple files associated to "+ regx[i] +":\n"+str(files_found[i])
            warnings.warn(msg)
    print("\nValidated! All outputs meet the requirements of '", keyword, "'\n")
    
    ## Parsing json files
    jsonk = [k for k, v in requir_dict.items() if v == 'json']
    requir_json = dict((k, requir_dict[k]) for k in jsonk)
    schemalist = [get_schema(benchmark, keyword, k) for k in requir_json.keys()]
    files_found_dict = dict(zip(requir_names, files_found))
    files_found_dict = dict((k, files_found_dict[k]) for k in jsonk)

    schemaToFiles = dict(zip(schemalist, files_found_dict.values()))

    for k in schemaToFiles.keys(): 
        if len( schemaToFiles[k]) == 1: 
            schemaToFiles[k] = data_folder + str(schemaToFiles[k][0])
        else: 
            schemaToFiles[k] = [data_folder + v for v in schemaToFiles[k]]

    ## Validation
    for k in schemaToFiles.keys(): 
        if isinstance(schemaToFiles[k], str): 
            print("Validation for ", schemaToFiles[k], "...")
            validate_json_file(schemaToFiles[k], k)
            print("OK!")
        elif isinstance(schemaToFiles[k], list): 
            for v in  schemaToFiles[k]: 
                print("Validation for ", v, "...")
                isOk = validate_json_file(v, k)
                if isOk == True: 
                    return True
                else:
                    msg = "File '"+ v + "' not following the requirements."
                    raise Exception(msg)
    
    return True




