__author__ = 'zhhuta'
import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="vpsnet",
    version="0.1.0",
    author="Vitaliy Zhhuta",
    author_email="vitaliyz@uk2group.com",
    description="Python wraper for vps.net api ",
    license=("BSD", "MIT"),
    keywords="vps.net api python",
    url="https://github.com/zhhuta/vpsnet",
    packages=['vpsnet'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: MIT License",
    ], requires=['requests']
)