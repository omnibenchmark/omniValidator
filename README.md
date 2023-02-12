# omniValidator

`omniValidator` is a python module to control file requirements in an Omnibenchmark project. 

## Usage

The following sections assume that your working directory is an Omnibenchmark project associated to an **existing** Omnibenchmark and stage (data, method, metric, etc.).

You can check [here](https://github.com/ansonrel/omniValidator/tree/main/src/omniValidator/schemas) if the Omnibenchmark you are working on has available validators. 

If you are working with an `Omnibenchmark` object, the main function (`omniValidator.validate_requirements`) can be used without other specifications. 

### Display the requirements

The requirements for a given Omnibenchmark module can be visualized with the following function: 

```
import omniValidator as ov
from omnibenchmark.utils.build_omni_object import get_omni_object_from_yaml
from omnibenchmark.renku_commands.general import renku_save

## Load config
omni_obj = get_omni_object_from_yaml('src/config.yaml')

## shows the requirements
ov.display_requirements(omni_obj = omni_obj)

```

which will render an html table of the requirements needed for the Omnibenchmark project you are working on. 

### Validate required files and JSON files

The `validate_all` function of `omniValidator` shows you how to check for: 

- output files needed for the downstream modules and if they are correctly generated and named

- JSON files that you created and if they are correctly formatted (ie, contain the required fields for downstream projects)

```
import omniValidator as ov
ov.validate_all(
    benchmark = 'omni_batch_py', 
    keyword = 'omni_batch_data', 
    data_folder = 'examples/csf-patients-py/data/csf_patient_py'
)
```

which will raise an `Exception` if an output file is missing or if a JSON file is badly formatted. 

### Validate required files only

The output files of an Omnibenchmark workflow can be validated by specifying an **`omnibenchmark` object**: 

```
import omniValidator as ov
from omnibenchmark.utils.build_omni_object import get_omni_object_from_yaml
from omnibenchmark.renku_commands.general import renku_save

## Load config
omni_obj = get_omni_object_from_yaml('src/config.yaml')

## Validates the output mapping
ov.validate_requirements(omni_obj = omni_obj)

```

Which will return a boolean (`True`) if valid and an `Exception` error if some output are missing. 

If multiple output are detected, you will get a warning message such as below: 

```
.../omniValidator/src/omniValidator/core.py:119: UserWarning: Multiple files associated to counts.*mtx.gz:
['csf_patient_py_counts (copy).mtx.gz', 'csf_patient_py_counts.mtx.gz']
```

It is highly advised to check your workflow if this happens as it might create issues in downstream steps. 

The output files of an Omnibenchmark workflow can also be validated with **manual specifications, assuming that the output files were already generated**: 

```
import omniValidator as ov
ov.validate_requirements(
    benchmark = 'omni_batch_py', 
    keyword = 'omni_batch_data', 
    data_folder = 'examples/csf-patients-py/data/csf_patient_py'
)
```

Validation requirements can be accessed on the [official repo of the module](https://github.com/omnibenchmark/omniValidator/tree/main/src/omniValidator/schemas). 

### Validate JSON files only

JSON files contain metadata and are used in most Omnibenchmark projects. The content and structure of JSON files  can be validated as follows: 


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

## How to modify requirements

You can modify existing requirements/ JSON schemas or add new ones using pull requests or by opening an issue on the Github page of the module. 

All schemas and requirements are in the [`src/omniValidator/schemas`](https://github.com/ansonrel/omniValidator/tree/main/src/omniValidator/schemas) folder of the module. 