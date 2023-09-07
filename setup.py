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
    description="zkp-playground is a playground for ZKP algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/oxor-io/zkp-playground',
    version='1.0.0',
    packages=find_packages(here, exclude=['tests', 'notes', 'docs']),
    license='GPL',
    author=author,
    author_email=email,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security :: Cryptography'
    ],
    entry_points={
        'console_scripts': [
            'zkp_playground=zkp_playground.client.shell:main'
        ]
    }
)
