from setuptools import setup, find_packages
from importlib.util import  module_from_spec, spec_from_file_location

spec = spec_from_file_location("constants", "./json_kit/_constants.py")
constants = module_from_spec(spec)
spec.loader.exec_module(constants)

with open('README.md', 'r') as fp:
    long_description = fp.read()

__author__ = constants.__author__
__url__ = constants.__url__
__version__ = constants.__version__
__license__ = constants.__license__

setup(
    name='json_kit',
    packages=find_packages(
        exclude=['*.tests', '*.test_.*', 'tests', 'develop']
    ),
    package_dir={},
    # metadata
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=__author__,
    url=__url__,
    version=__version__,
    license=__license__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)