from setuptools import setup, find_packages

requires = [
    'tropofy',
    'requests',
    'simplekml',
]

setup(
    name='foodr',
    version='1.0',
    description='Finds you the optimal lunch :)',
    author='Melody Kelly',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
