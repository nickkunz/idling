## libraries
import os
import configparser
from dotenv import load_dotenv

## ini configs
def ini_con(file, sect):

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

    ## load configs
    config = configparser.ConfigParser()
    config.read(file)

    keys = dict()
    for i in config[sect]:
        value = config.get(sect, i)
        keys[i] = value

    return keys

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

    vars = dict()
    for i in os.environ:
        vars[i] = os.environ[i]

    return vars
