import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


install_requires = [
    line
    for line in open(
        os.path.join(here, "requirements.txt"),
        "r"
    )
]


setup(
    name='klefki',
    version='0.0.1',
    packages=find_packages(here, exclude=['tests']),
    license='MIT',
    description='',
    install_requires=install_requires,
)
