import os
from setuptools import setup

requirements = []
requirements_path = 'etc/setuptools/requirements.txt'
if os.path.exists(requirements_path):
    with open(requirements_path) as requirements_file:
        requirements = requirements_file.read().splitlines()
        if len(requirements) == 0:
            raise Exception("Failed to load requirements from {}".format(requirements_path))

setup(
    name                    = "BuildingSimulator",
    version                 = "0.1",
    install_requires        = requirements,
    include_package_data    = True,
    zip_safe                = False,
    packages                = [ 'sim', 'sim.models', 'sim.test'],
    scripts = [
        'bin/run-tests',
        'bin/run-sim',
        ],
    test_suite              = "sim.test.full_suite"
)
