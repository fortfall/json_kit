from setuptools import setup, find_packages

setup(
    name='json_encoders',
    version='1.0',
    author='lihailin',
    packages=find_packages(
        exclude=['*.tests', '*.test_.*', 'tests', 'develop']
    )
)