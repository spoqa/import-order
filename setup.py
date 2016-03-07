from setuptools import find_packages, setup

from import_order.version import VERSION


install_requires = [
    'Pygments >= 2.0.2, < 2.1.0',
]


tests_require = [
    'pytest >= 2.7.0',
    'tox',
]


def readme():
    with open('README.rst') as f:
        try:
            return f.read()
        except (IOError, OSError):
            return None


setup(
    name="import-order",
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/spoqa/import-order',
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'tests': tests_require,
    },
    maintainer='Spoqa',
    maintainer_email='dev' '@' 'spoqa.com',
    entry_points={
        'console_scripts': [
            'import-order = import_order.cli:main',
        ]
    },
    description='Check python import order.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ]
)
