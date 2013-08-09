from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.registry import Registry

_REGISTRY = Registry.Registry('remote command')

get = _REGISTRY.get
function = _REGISTRY.function
register = _REGISTRY.register
register_all = _REGISTRY.register_all
