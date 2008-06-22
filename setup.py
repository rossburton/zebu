#!/usr/bin/env python

from distutils.core import setup

setup(name='Zebu',
      version="0.1",
      description="Cowbuilder Manager",
      author="Ross Burton",
      author_email="ross@burtonini.com",
      url="http://www.burtonini.com/",
      
      scripts=["zebu"],
      data_files=[
        ("share/applications", ["zebu.desktop"]),
        ("share/icons/hicolor/16x16/apps", ["icons/16x16/zebu.png"]),
        ("share/icons/hicolor/22x22/apps", ["icons/22x22/zebu.png"]),
        ("share/icons/hicolor/32x32/apps", ["icons/32x32/zebu.png"]),
        ("share/icons/hicolor/48x48/apps", ["icons/48x48/zebu.png"]),
        ("share/icons/hicolor/scalable/apps", ["icons/scalable/zebu.svg"]),
        ]
      )
