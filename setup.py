from setuptools import setup, find_packages


setup(
    name='BaMMI',
    version='0.1.9',
    author='Roy Peleg',
    description='Basic Mind-Machine Interface.',
    packages=find_packages(where='BaMMI'),
    package_dir={"": "BaMMI"},
    install_requires=[
        'Click==7.0',
        'codecov==2.0.15',
        'Flask==1.1.1',
        'matplotlib==3.2.1',
        'numpy==1.18.2',
        'pika==1.1.0',
        'Pillow==7.1.1',
        'protobuf==3.11.3',
        'pytest==5.3.2',
        'pytest-cov==2.8.1',
        'pymongo==3.10.1',
        'requests==2.23.0'
    ],
    tests_require=['pytest', 'pytest-cov'],
    python_requires='>=3.8',
)
