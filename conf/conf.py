## libraries
import os
import configparser
from dotenv import load_dotenv


## ini section keys
def ini_key(file, sect):

    """
    Desc:
        Loads a configuration file in .ini format and returns a dictionary
        containing the key-value pairs of the specified section.

    Args:
        file (str): The path of the .ini configuration file.
        sect (str): The name of the section witin the .ini file.

    Returns:
        dict: A dictionary containing the key-value pairs of the specified 
        section.

    Raises:
        TypeError: The argument 'file' is not a string.
        TypeError: The argument 'sect' is not a string.
    """

    ## arg check
    if not isinstance(file, str):
        raise TypeError("The 'file' argument must be a string.")
    
    if not isinstance(sect, str):
        raise TypeError("The 'sect' argument must be a string.")

    ## load ini file
    config = configparser.ConfigParser()
    config.read(file)

    ## output keys
    keys = dict()
    for i in config[sect]:
        value = config.get(sect, i)
        keys[i] = value

    return keys


## ini section names
def ini_var(file, sect):

    """
    Desc:
        Loads an .ini configuration file and returns a list of the last three
        characters of each variable name in the specified section.

    Args:
        file (str): The path of the .ini configuration file.
        sect (str): The name of the section within the .ini file.

    Returns:
        list: A list containing the last three characters of each variable name
        in the specified section.

    Raises:
        TypeError: If the argument 'file' is not a string.
        TypeError: If the argument 'sect' is not a string.
    """

    ## arg check
    if not isinstance(file, str):
        raise TypeError("The 'file' argument must be a string.")
    
    if not isinstance(sect, str):
        raise TypeError("The 'sect' argument must be a string.")

    ## load ini file
    config = configparser.ConfigParser()
    config.read(file)

    ## three code variable names
    return [i[-3:] for i in config[sect]]


## env variables
def env_var(file):

    """
    Desc:
        Loads environment variables from .env file and returns them as a 
        dictionary.

    Args:
        file (str): The path of the .env file.

    Returns:
        dict: A dictionary containing the environment variables.

    Raises:
        TypeError: The argument 'file' is not a string.
    """

    ## arg check
    if not isinstance(file, str):
        raise TypeError("The 'file' argument must be a string.")

    ## load env vars
    load_dotenv(file)

    ## output vars
    vars = dict()
    for i in os.environ:
        vars[i] = os.environ[i]

    return vars
