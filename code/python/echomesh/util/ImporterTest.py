"""
>>> import sys
>>> sys2 = Importer.imp('sys')
>>> assert sys is sys2

>>> wombat = Importer.imp('wombat')
>>> print_exception(wombat)
You requested a feature that needs the Python library "wombat".

"""

from echomesh.util import Importer

def print_exception(wombat):
  try:
    wombat.test
  except Exception as e:
    print(e)
  else:
    print('FAILED')