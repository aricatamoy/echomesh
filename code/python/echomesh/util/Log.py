"""Typical usage:  at the top of your file, put:

LOGGER = Log.logger(__name__)
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import logging.config
import sys
import traceback

FORCE_DEBUG = not not True
VDEBUG = 5

LOG_LEVEL = 'INFO'

DEFAULT_FORMAT = '%(message)s'
DEBUG_FORMAT = '%(message)s'
FILE_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'

_LOG_SIGNATURE = 'util/Log.py'
_ERROR_COUNTER = {}

def _check_error_count(limit, every):
  for line in traceback.format_stack():
    if _LOG_SIGNATURE not in line:
      errors = _ERROR_COUNTER.get(line, 0)
      if limit is not None and errors >= limit * (every or 1):
        return False
      _ERROR_COUNTER[line] = errors + 1
      return not (every and (errors % every))

def _add_level_vdebug():
  logging.addLevelName(VDEBUG, 'VDEBUG')

  def vdebug(self, message, *args, **kws):
    self.log(VDEBUG, message, *args, **kws)

  logging.Logger.vdebug = vdebug
  logging.VDEBUG = VDEBUG

_add_level_vdebug()

class _ConfigClient(object):
  def config_update(self, get):
    get = get or (lambda *x: None)
    self.debug = FORCE_DEBUG or get('debug')
    self.stack_traces = self.debug or get('diagnostics', 'stack_traces')
    self.log_level = (get('logging','level') or LOG_LEVEL).upper()
    if self.debug:
      if self.log_level not in ['DEBUG', 'VDEBUG']:
        self.log_level = 'DEBUG'

    self.kwds = {u'level': getattr(logging, self.log_level)}
    self.filename = get('logging', 'file')
    if self.filename:
      self.kwds[u'filename'] = self.filename
    else:
      self.kwds[u'stream'] = sys.stdout

    self.kwds[u'format'] = get('logging', 'format') or (
      FILE_FORMAT if self.filename else
      DEBUG_FORMAT if self.debug
      else DEFAULT_FORMAT)

    self.kwds = dict((str(k), v) for k, v in self.kwds.iteritems())
    logging.basicConfig(**self.kwds)


_CONFIG = _ConfigClient()
try:
  from echomesh.base import Config
except:
  _CONFIG.config_update(None)
else:
  Config.add_client(_CONFIG)

def logger(name=None):
  assert name
  log = logging.getLogger(name or 'echomesh')
  original_error_logger = log.error

  def new_error_logger(*args, **kwds):
    limit = kwds.pop('limit', None)
    every = kwds.pop('every', None)
    raw = kwds.pop('raw', None)

    if limit is not None or limit is not None:
      if not _check_error_count(limit, every):
        return

    message, args = (args[0] if args else ''), args[1:]
    exc_type, exc_value = sys.exc_info()[:2]
    if exc_type and not raw:
      message = '%s %s' % (exc_value, message)
      kwds['exc_info'] = kwds.get('exc_info', _CONFIG.stack_traces)
    if not _CONFIG.filename:
      message = 'ERROR: %s\n' % message
    original_error_logger(message, *args, **kwds)

  log.error = new_error_logger
  return log

LOGGER = logger(__name__)
LOGGER.debug('\nLog level is %s', _CONFIG.log_level)

