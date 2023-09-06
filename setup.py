import os
import platform
from setuptools import setup, find_packages, Extension

here = os.path.abspath(os.path.dirname(__file__))
platform = platform.python_implementation()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
    line
    for line in open(
        os.path.join(here, "requirements.txt"),
        "r"
    )
]
author = 'oxorio'
email = 'ping@oxor.io'


setup(
    name='zkp-playground',
    description="zkp-playground is a library for researching elliptic curve group based algorithms & applications, such as MPC, HE, ZKP, and Bitcoin/Ethereum. All data types & structures are based on mathematical defination of abstract algebra.",  # noqa
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/oxor-io/zkp-playground',
    version='1.0.0',
    packages=find_packages(here, exclude=['tests', 'notes']),
    license='GPL',
    author=author,
    author_email=email,
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Console',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography"
    ],
    entry_points={
        'console_scripts': [
            'zkp_playground=zkp_playground.client.shell:main'
        ]
    }
)
