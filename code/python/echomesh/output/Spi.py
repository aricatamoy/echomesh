from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.color import Combine
from echomesh.color import SetupDebianSpiLights
from echomesh.expression import Expression
from echomesh.output.Output import Output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

DEFAULT_SPI_DEVICE = '/dev/spidev0.0'
DEFAULT_GAMMA = 2.5

_LATCH_COUNT = 3

EMULATION_FILE = '/tmp/spi-emulation.txt'

class Spi(Output):
  def RGB(r, g, b):
    return r, g, b

  def GRB(r, g, b):
    return g, r, b

  def BRG(r, g, b):
    return b, r, g

  def __init__(self, count=None, rgb_order='rgb', device=DEFAULT_SPI_DEVICE,
               gamma=DEFAULT_GAMMA, **description):
    self.enabled = SetupDebianSpiLights.lights_enabled()
    if not self.enabled:
      LOGGER.error('SPI running in emulation mode.')
    self.gamma = gamma
    self.rgb_order = getattr(Spi, rgb_order.upper(), None)
    if not self.rgb_order:
      raise Exception('Don\'t understand rgb_order=%s' % rgb_order)

    Config.add_client(self)
    self.count_set = count is not None
    if self.count_set:
      self._set_count(count)
    self._device = open(device, 'wb')
    self.finish_construction(description, is_redirect=False)

  def config_update(self, get):
    if not self.count_set:
      self.count = get('light', 'count')
      self._set_count()
    self.brightness = Expression.convert(get('light', 'brightness'))

  def _write(self):
    if self.enabled:
      self._device.write(self.lights)
      self._device.flush()
    elif not getattr(self, 'emulation_written'):
      self.emulation_written = True
      with open(EMULATION_FILE, 'w') as f:
        f.write(str(self.lights))

  def _set_count(self, count):
    self.count = count
    self.lights = bytearray(0 for i in xrange(3 * count + _LATCH_COUNT))
    for i in xrange(_LATCH_COUNT):
      self.lights[-1 - i] = 0

  def emit_output(self, data):
    lights = Combine.combine(data)
    lights.scale(self.brightness)
    lights.gamma(self.gamma)

    for i, light in enumerate(lights):
      light_bytes = self.rgb_order(*light.rgb_range(128, 256))
      self.lights[3 * i: 3 * (i + 1)] = light_bytes

    self._write()
