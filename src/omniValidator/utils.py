import os as os
import warnings

def get_avail_benchmarks():
    """
    Lists available benchmarks in omniValidator.
    """
    from omniValidator import __path__ as omni_val_path  
    out =  os.listdir(os.path.join(omni_val_path[0], 'schemas' ))
    out.remove("README.md")
    return out

def get_avail_keywords(benchmark=None):
    """
    Lists available keywords in omniValidator for a given benchmark.
    """
    from omniValidator import __path__ as omni_val_path 
    if benchmark is None: 
            msg = "benchmark has to be specified"
            raise Exception(msg)
    out =  os.listdir(os.path.join(omni_val_path[0], 'schemas', benchmark ))
    return out


def schema_exist(benchmark=None, keyword=None): 
    """
    Checks if the provided benchmark (and keyword) have a defined schema. 

    Returns: 
        Raises:
         - a warning if the benchmark doesn't exist yet; likely a WIP benchmark. 
         - an error if the keyword doesn't exist; benchmark is active so the missing keyword is likely due to a wrong keyword or a missing part in omniValidator that needs to be  filled-
    """
    from omniValidator import __path__ as omni_val_path  
    if benchmark is None or keyword is None: 
        msg = "Benchmark and keyword has to be specified"
        raise Exception(msg)

    ## Check benchmark exist
    out_bench = os.path.join(omni_val_path[0], 'schemas', benchmark )
    if not os.path.isdir(out_bench): 
        msg = "Benchmark is not specified "
        warnings.warn(msg)

    ## Check keyword exist
    out_key = os.path.join(omni_val_path[0], 'schemas', benchmark, keyword)
    if not os.path.isdir(out_key): 
        msg = "Keyword not defined in omniValidator or not correctly specified. \nPlease use one of the followings or add a new one to omniValidator:\n"
        msg += ",".join(get_avail_keywords(benchmark))
        raise Exception(msg)
