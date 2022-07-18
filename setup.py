#!/usr/bin/env python

from distutils.core import setup
from pathlib import Path

from setuptools import find_packages

about = {}
cwd = Path(__file__).parent.absolute()
with open(cwd / "euskalmet" / '__version__.py', 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

packages = find_packages()

with open(cwd / 'requirements.txt', 'r') as f:
    requires = f.read().splitlines()

setup(
    name="python-euskalmet",
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    # package_data={'': ['LICENSE', 'NOTICE']},
    # include_package_data=True,
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.8',
    install_requires=requires,
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='euskalmet weather api euskadi "basque contry" opendata',
    project_urls={  # Optional
        'Bug Reports': 'https://gitlab.com/r3v1/python-euskalmet/issues',
    },
)
