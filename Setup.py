#!/usr/bin/env python

from distutils.core import setup
from os import listdir
from os.path import join

setup(name='HadoopLogTools',
      version='1.0',
      description='Tools for Hadoop logs analisys',
      author='Mario Pastorelli',
      author_email='pastorelli.mario@gmail.command',
      url='',
      scripts=[join('bin',f) for f in listdir('bin')],
      packages=['hadoop.log'
               ,'hadoop.log.convert'
               ,'hadoop.util'
               ,'hadoop.plot'],
     )
