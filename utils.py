import ConfigParser
import os

def parse_config(config_filename):
    configParser = ConfigParser.ConfigParser()
    configParser.read(config_filename)

    config = {}
    for section in configParser.sections():
        entries = configParser.items(section)
        for (key, value) in entries:
            config[key] = value            
    return config
