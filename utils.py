import ConfigParser
import datetime
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

def parse_header(raw_header):
    parsed_header = {}
    for line in raw_header.splitlines():
        try:
            (key, value) = line.split(":", 1)
        except ValueError:
            raise Exception("The header %s is not in proper format, Use 'Key:Value' format" % line)
        parsed_header[key.strip().lower()] = value.strip()
    return parsed_header

def parse_timestamp(timestamp):
  """
  Parses a 'Day, DD MM YYYY HH:MM:SS +TZ' entry.
  """

  try:
      timestamp = ' '.join(timestamp.split()[:-1])
      timestamp = datetime.datetime.strptime(timestamp, "%a, %d %b %Y %H:%M:%S")
      return timestamp
  except ValueError:
      raise ValueError("Timestamp wasn't parseable: %s" % timestamp)
