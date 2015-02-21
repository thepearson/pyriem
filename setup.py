# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search('^__VERSION__\s*=\s*"(.*)"', open('pyriem/pyriem.py').read(), re.M).group(1)


with open("README.md", "rb") as f:
    long_descr=f.read().decode("utf-8")


setup(
    name="pyriem",
    packages=["pyriem"],
    entry_points={
        "console_scripts": ['pyriem=pyriem.pyriem:main']
        },
    install_requires=['argparse', 'bernhard', 'pyyaml', 'psutil'],
    include_package_data=True,
    version = version,
    description="A statistics collection framework for Riemann.",
    long_description=long_descr,
    author="Craig Pearson",
    author_email="thepearson@gmail.com",
    url="http://hauntdigital.co.nz",
    )
