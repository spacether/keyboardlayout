from setuptools import setup, find_packages

version = {}
with open("keyboardlayout/version.py") as fp:
    exec(fp.read(), version)

setup(
    name = 'keyboardlayout',
    install_requires = ['PyYAML >= 5.3.1', 'pygame >= 2.0.0'],
    python_requires='>=3',
    version = version['__version__'],
    description = 'A python library to display different keyboards',
    author = 'Justin Black',
    packages = find_packages(),
    package_data={'keyboardlayout': ['keyboardlayout/layouts/*.yaml']},
    url = "https://github.com/spacether/keyboardlayout",
    entry_points = {},
    license='see LICENSE.txt',
    keywords = ["keyboard", "qwerty", "layout", "azerty"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'dev': [
            'sphinx',
            'pytest',
        ]
    },
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Topic :: Games/Entertainment :: Simulation',
    ],
    long_description = 'A python library to display different keyboards'
)
