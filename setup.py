#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='GeneaTD',
    version='1.0',
    author='Frederic Kerber, Pascal Lessel, Michael Mauderer',
    author_email='info@geneatd.de',
    url='http://www.dfki.de/geneatd/index_en.html',
    license='GPL',
    packages=['geneatd'],
    scripts=['scripts/geneatd'],
    package_data={
            'geneatd': ['resources/*.png', 'resources/*.jpg', 'resources/hp/*.png',
                    'resources/labels/*.png', 'resources/soundfiles/*.mp3', 'fonts/*'],
    }
)

