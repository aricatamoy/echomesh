#!/usr/bin/env python

## Run python setup.py build_ext to build echomesh.so

import os

import platform

from distutils.core import setup, Command, Extension
from Cython.Build import cythonize

DEBUG = True

PLATFORM = platform.system().lower()

IS_LINUX = (PLATFORM == 'linux')
IS_MAC = (PLATFORM == 'darwin')
IS_WINDOWS = (PLATFORM == 'windows')

assert IS_LINUX or IS_MAC or IS_WINDOWS

if IS_MAC:
  EXTRA_COMPILE_ARGS = ('-x c++ -arch x86_64 -fmessage-length=0 -std=c++11 '
                        '-IJuceLibraryCode'.split(' '))
  EXTRA_LINK_ARGS = '-framework Cocoa -framework WebKit'.split(' ')

  if DEBUG:
    EXTRA_COMPILE_ARGS += ('-O0 -D_DEBUG=1 -DDEBUG=1 ' +
                           '-DJUCER_XCODE_MAC_F6D2F4CF=1').split(' ')
    LIBRARY = 'echomesh-debug'
    LIB_DIR = '/development/echomesh/code/cython/Builds/MacOSX/build/Debug'

  else:
    EXTRA_COMPILE_ARGS += ('-O2'.split(0))
    LIBRARY = 'echomesh'
    LIB_DIR = '/development/echomesh/code/cython/Builds/MacOSX/build/Release'

elif IS_LINUX:
  raise Exception("Can't build for Linux")

elif IS_WINDOWS:
  raise Exception("Can't build for Windows")

else:
  raise Exception("Don't understand platform %s." % platform)

lib = Extension(
  LIBRARY,
  ['echomesh.pyx'],
  library_dirs=[LIB_DIR],
  libraries=['echomesh'],
  extra_compile_args=EXTRA_COMPILE_ARGS,
  extra_link_args=EXTRA_LINK_ARGS,
  )

class CleanCommand(Command):
  description = "custom clean command that forcefully removes dist/build directories"
  user_options = []
  def initialize_options(self):
    self.cwd = None

  def finalize_options(self):
    self.cwd = os.getcwd()

  def run(self):
    assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
    os.system('rm -Rf %s.so ./build ./dist' % LIBRARY)

setup(
  name='Echomesh',
  ext_modules=cythonize([lib]),
  cmdclass={'clean': CleanCommand},
  )
