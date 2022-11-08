# omniValidator

Python module to check files in an Omnibenchmark.

## Usage

### Validate required files

Assuming that your working directory is an Omnibenchmark project associated to an **existing** Omnibenchmark and stage (data, method, metric, etc.), the outputs can be validated as follows: 

```
import omniValidator as ov
ov.validate_requirements(benchmark = "omni_batch_py", keyword = "omni_batch_data", data_folder = "data/csf_patient_py")
```
which will return an error message if any output is missing. 

If multiple output are detected, you will get a warning message such as below: 

```
.../omniValidator/src/omniValidator/core.py:119: UserWarning: Multiple files associated to counts.*mtx.gz:
['csf_patient_py_counts (copy).mtx.gz', 'csf_patient_py_counts.mtx.gz']
```

It is highly advised to check your workflow if this happens as it might create issues in downstream steps. 

###


## Contribute

