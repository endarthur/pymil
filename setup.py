#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pymil",
    version="0.2.0",
    py_modules=['pymil'],
    entry_points={'console_scripts': [
        'pymil = pymil:main',
    ]},
    author="Arthur Endlein",
    author_email="endarthur@gmail.com",
    description=(
        "A basic Open-source Carte internationale du Monde au Millionième nomenclature encoder."
    ),
    license="GPL",
    keywords="cartography maps GIS",
    url="https://github.com/endarthur/pymil",
    long_description=read('README.rst'),
    dowload_url="https://github.com/endarthur/pymil/archive/0.2.0.tar.gz",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering :: GIS",
    ], )
