from setuptools import setup, find_packages

from import_order.version import VERSION


install_requires = [
    'Pygments >= 2.0.2, < 2.1.0',
]

setup(
    name="import-order",
    version=VERSION,
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'import-order = import_order.cli:main',
        ]
    },
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
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ]
)
