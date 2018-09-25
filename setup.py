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
author = 'Ryan Kung'
email = 'ryankung@ieee.org'


setup(
    name='klefki',
    description='Klefki is a playground for researching elliptic curve group based cryptocoins, such as Bitcoin and Ethereum. All data types & structures are based on mathematical defination of abstract algebra.',  # noqa
    url='https://github.com/RyanKung/klefki',
    version='0.0.4.0',
    packages=find_packages(here, exclude=['tests']),
    license='GPL',
    author=author,
    author_email=email,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    entry_points={
        'console_scripts': [
            'klefki=klefki.client.shell:main'
        ]
    }
)
