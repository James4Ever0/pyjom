#!/usr/bin/env python
import io
import os.path
from setuptools import setup
# allow proxy
import os

os.environ["http_proxy"] =""
os.environ["https_proxy"] =""

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

setup(
    name="kaldiio",
    version="2.17.2",
    description="Kaldi-ark loading and writing module",
    author="nttcslab-sp",
    # author_email='',
    url="https://github.com/nttcslab-sp/kaldiio",
    long_description=io.open(
        os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8"
    ).read(),
    long_description_content_type="text/markdown",
    packages=["kaldiio"],
    install_requires=["numpy","pytest-runner"], # whatever. we just install this fucker
    setup_requires=[],
    tests_require=["pytest", "pytest-cov", "soundfile"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
)
