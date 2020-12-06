import sys
import classes.log as log

class Options(object):

   def __init__(self):
      options = sys.argv
      self.__options = {}
      for option in options:
         optParts = option.split("=", 1)
         if len(optParts) != 2:
            continue
         self.__options[optParts[0]] = optParts[1]

   def getOptions(self):
      return self.__options

   def get(self, key):
      return self.__options[key] if key in self.__options else False

   def set(self, key, value):
      self.__options[key] = value

