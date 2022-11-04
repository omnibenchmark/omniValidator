import json 

def schema_validate():
    """
    """
    return("ok")


def validateJSON(jsonData):
    """
    Returns False if input can not be decoded as JSON. 
    """
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

