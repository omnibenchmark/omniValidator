# omniValidator

Python module to check files in an Omnibenchmark.

## Usage

The following sections assume that your working directory is an Omnibenchmark project associated to an **existing** Omnibenchmark and stage (data, method, metric, etc.).

### Validate required files and JSON files

The `validate_all` function of `omniValidator` shows you how to check: 

- That all output files needed for the downstream modules were correctly generated and named

- that the JSON files that you created are correctly formated and contain the required fields

```
import omniValidator as ov
ov.validate_all(
    benchmark = 'omni_batch_py', 
    keyword = 'omni_batch_data', 
    data_folder = 'examples/csf-patients-py/data/csf_patient_py'
)

```

### Validate required files only

The output files of an Omnibenchmark workflow can be validated as follows: 

```
import omniValidator as ov
ov.validate_requirements(
    benchmark = 'omni_batch_py', 
    keyword = 'omni_batch_data', 
    data_folder = 'examples/csf-patients-py/data/csf_patient_py'
)
```
which will return an error message if any output is missing. 

If multiple output are detected, you will get a warning message such as below: 

```
.../omniValidator/src/omniValidator/core.py:119: UserWarning: Multiple files associated to counts.*mtx.gz:
['csf_patient_py_counts (copy).mtx.gz', 'csf_patient_py_counts.mtx.gz']
```

It is highly advised to check your workflow if this happens as it might create issues in downstream steps. 

Validation requirements can be accessed on the [official repo of the module](https://github.com/ansonrel/omniValidator/tree/main/src/omniValidator/schemas). 

### Validate JSON files only

JSON files contain metadata and are used in most Omnibenchmark projects. The output JSON files of a project can be validated as follows: 


```
import omniValidator as ov

## Retrieve the schema validator associated with your project
sch = ov.get_schema(
    benchmark = 'omni_batch_py', 
    keyword = 'omni_batch_data', 
    ftype = 'data_info'
)
## Validate your JSON file
ov.validate_json_file(
    json_input_path = 'examples/csf-patients-py/data/csf_patient_py/csf_patient_py_data_info_CORRECT.json', 
    json_schema_path = sch
)
```

Which returns a boolean (`True`) if your JSON is valid. 

## Contribute

You can modify existing requirements/ JSON schemas or add new ones using pull requests or by opening an issue on the Github page of the module. 

### New requirements for a Omnibenchmark stage

Either by PR or by opening a new issue on github. 