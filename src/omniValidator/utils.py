import os as os
import warnings
import requests

def get_github_directory_list(username = "omnibenchmark", repos = "omni_essentials", folder = ""):
    # Extract the username and repository name from the GitHub URL

    # Make the API request to get the repository contents
    api_url = os.path.join("https://api.github.com/repos", 
    username, repos, "contents", folder)
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the JSON response
        data = response.json()

        # Filter the directories from the response
        directories = [item['name'] for item in data if item['type'] == 'dir']

        return directories
    else:
        # If the request was not successful, raise an exception or handle the error accordingly
        response.raise_for_status()


def get_avail_benchmarks(folder = "schemas"):
    """
    Lists available benchmarks in omni-essentials.
    """
    out =  get_github_directory_list(folder = folder)
    return out

def get_avail_keywords(folder = "schemas", benchmark=None):
    """
    Lists available keywords in omniValidator for a given benchmark.
    """
    if benchmark is None: 
            msg = "benchmark has to be specified"
            raise Exception(msg)
    out =  get_github_directory_list(folder = os.path.join(folder, benchmark))
    return out


def schema_exist(benchmark=None, keyword=None, folder = "schemas"): 
    """
    Checks if the provided benchmark (and keyword) have a defined schema. 

    Returns: 
        Raises:
         - a warning if the benchmark doesn't exist yet; likely a WIP benchmark. 
         - an error if the keyword doesn't exist; benchmark is active so the missing keyword is likely due to a wrong keyword or a missing part in omniValidator that needs to be  filled-
    """
    if benchmark is None or keyword is None: 
        msg = "Benchmark and keyword has to be specified"
        raise Exception(msg)

    ## Check benchmark exist
    try:
        out_bench = get_github_directory_list(folder = os.path.join(folder, benchmark))
    except: 
        msg = "Benchmark does not exist "
        warnings.warn(msg)
        return
    
    # Check keyword exist
    try: 
        out_key = get_github_directory_list(folder = os.path.join(folder, benchmark, keyword))
    except: 
        msg = "Keyword not defined in omniValidator or not correctly specified. \nPlease use one of the followings or add a new one to omniValidator:\n"
        msg += ",".join(get_avail_keywords(benchmark = benchmark))
        raise Exception(msg) 
    
    return True
    

   
        
