from setuptools import setup, find_packages

from importlib.util import  module_from_spec, spec_from_file_location
spec = spec_from_file_location("./json_encoders/_constants.py")
constants = module_from_spec(spec)
spec.loader.exec_module(constants)

setup(
    name='json_encoders',
    packages=find_packages(
        exclude=['*.tests', '*.test_.*', 'tests', 'develop']
    ),
    package_dir={},
    # metadata
    author=constants.__author__,
    url=constants.__url__,
    version=constants.__version__,
    license=constants.__license__
)