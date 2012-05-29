import sys
from setuptools import setup

import bossman

# versions are nearly arbitrary, may work with older versions
requirements = ['Twisted==12.0.0', 'clint==0.3.1']
if sys.version_info[:2] in ((2, 6), (3, 1)):
    # argparse has been added in Python 3.2 / 2.7
    requirements.append('argparse>=1.2.1')

setup(
    name='bossman',
    version=bossman.__version_str__,
    description=bossman.__doc__.strip(),
    author='Yaniv Aknin',
    author_email='yaniv@aknin.name',
    packages=['bossman'],
    url='https://github.com/yaniv-aknin/bossman',
    entry_points={
        'console_scripts': [
            'bossman = bossman.main:main',
        ],
    },
    license=bossman.__licence__,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: System :: Systems Administration',
    ],
)
