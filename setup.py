from setuptools import setup

setup(
    name='sternum',
    version='0.0.1',
    package_dir={"": "src"},
    install_requires=[],
    setup_requires=[],
    entry_points={
        'console_scripts': [
            'sternum=__init__:run'
        ]
    }
)
