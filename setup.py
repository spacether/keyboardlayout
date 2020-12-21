from setuptools import setup, find_packages
import pathlib

this_directory = pathlib.Path(__file__).parent
with open(this_directory / 'README.md', encoding='utf-8') as f:
    long_description = f.read()

version = {}
with open(this_directory.joinpath('keyboardlayout', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name = 'keyboardlayout',
    install_requires = ['PyYAML >= 5.3.1'],
    python_requires='>=3.7',
    version = version['__version__'],
    description = 'A python library to display different keyboards',
    author = 'Justin Black',
    packages = find_packages(),
    package_data={'keyboardlayout': ['layouts/*.yaml']},
    url = "https://github.com/spacether/keyboardlayout",
    keywords = [
        "keyboard",
        "qwerty",
        "layout",
        "azerty",
        "pygame",
        "tkinter",
        "accessibility"
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pygame'],
    extras_require={
        'dev': [
            'sphinx',
            'setuptools',
            'wheel',
            'twine',
        ]
    },
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Games/Entertainment :: Simulation',
        'Development Status :: 5 - Production/Stable',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
