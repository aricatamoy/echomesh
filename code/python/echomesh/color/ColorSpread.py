from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import Color

from echomesh.color import ColorConv
from echomesh.util import Importer
from cechomesh import Transform

numpy = Importer.imp('numpy')

def color_spread(begin, end, steps, transform=None, use_hsv=True):
  if use_hsv:
    colors = ColorConv.rgb_to_hsv([begin, end]).T
  else:
    colors = numpy.array([begin, end]).T
  steps = int(steps)
  if transform:
    fn, fi = transform.apply, transform.inverse
    step_array = [fi(numpy.linspace(fn(s), fn(f), steps)) for s, f in colors]
  else:
    step_array = [numpy.linspace(s, f, steps) for s, f in colors]
  if use_hsv:
    step_array = ColorConv.hsv_to_rgb(numpy.array(step_array).T)
  else:
    step_array = numpy.array(step_array).T
  return step_array

def color_name_spread(begin=None, end=None, steps=None, transform=None):
  transform = transform and Transform(transform)

  # TODO: disallow these defaults?
  return color_spread(Color(begin or 'black').parts,
                      Color(end or 'white').parts,
                      steps or 2, transform=transform)
