from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import sys

from echomesh.base import Args
from echomesh.base import CommandFile
from echomesh.base import GetPrefix
from echomesh.base import Merge
from echomesh.base import Yaml

_ARGUMENT_ERROR = """
ERROR: Didn't understand arguments to echomesh: "%s".

echomesh needs to be called with arguments looking like "name=value".

Examples:
  echomesh
  echomesh debug=true
  echomesh audio.input.enable=false light.enable=false
"""

_ASSIGNMENT_ERROR = """
ERROR: couldn't assign a variable from: "%s".

Variable assignments look like "name=value" and you can have more than one
per line.

Examples:
  debug=true
  audio.input.enable=false light.enable=false
"""

class MergeConfig(object):
  def __init__(self):
    self.read()

  def read(self):
    self._read_file_configs()
    self.arg_config = self._assignment_to_config(sys.argv[1:], _ARGUMENT_ERROR)
    return self.recalculate()

  def recalculate(self):
    self.config = None
    self.changed = {}
    for f, configs in self.file_configs:
      self.config = Merge.merge(self.config, *configs)
      self.changed = Merge.merge(self.changed, *configs[2:])

    arg = copy.deepcopy(self.arg_config)
    clean_arg = Merge.difference_strict(arg, self.changed)
    Merge.merge_for_config(self.config, clean_arg)

    return self.config

  def assign(self, args, index=-1):
    configs = self.file_configs[index][1]  # default is 'master'
    while len(configs) < 3:
      configs.append({})
    Merge.merge(configs[2], self._assignment_to_config(args, _ASSIGNMENT_ERROR))
    return self.recalculate()

  def save(self):
    saved_files = []
    for f, configs in self.file_configs:
      if len(configs) > 2:
        saved_files.append(f)
        Merge.merge(*configs[1:])
        with open(f, 'r') as file:
          data = file.read().split(Yaml.SEPARATOR)[0]

        with open(f, 'wb') as file:
          file.write(data)
          file.write(Yaml.SEPARATOR)
          file.write(Yaml.encode_one(configs[1]))

    self.arg_config = Merge.difference_strict(self.arg_config, self.changed)
    self.recalculate()
    return saved_files

  def assignments(self, index=-1):
    assigned = self.file_configs[index][1]
    return (len(assigned) > 2 and GetPrefix.leafs(assigned[2])) or {}

  def _read_file_configs(self):
    self.file_configs = []
    base_config = None

    for f in reversed(CommandFile.expand('config.yml')):
      configs = Yaml.read(f, 'config')
      for c in configs:
        if base_config:
          Merge.merge_for_config(base_config, c)
        else:
          base_config = copy.deepcopy(c)
      self.file_configs.append([f, configs])

  def _assignment_to_config(self, args, error):
    arg = ' '.join(args)
    config = {}
    base_config = self.file_configs[0][1][0]
    assert isinstance(base_config, dict)
    try:
      for address, value in Args.split(arg):
        GetPrefix.set_assignment(address, value, base_config, config,
                                 unmapped_names=Merge.CONFIG_EXCEPTIONS)
      return config

    except Exception as e:
      e.arg = arg
      raise
