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
      install_required=[
         'numpy == 1.7.1'
        ,'matplotlib == 1.2.1'
        ,'scipy == 0.11.0'
        ],
      packages=['hadoop'
               ,'hadoop.log'
               ,'hadoop.log.convert'
               ,'hadoop.util'
               ,'hadoop.plot'],
     )
