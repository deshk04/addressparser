"""
  Author:         
  Create date:    
  Description:    singleton pattern class

  Version     Date                Description(of Changes)
  1.0                             Created
"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
