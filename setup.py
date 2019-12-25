from setuptools import setup, find_packages


setup(
    name='BaMMI',
    version='0.1.0',
    author='Roy Peleg',
    description='Basic Mind-Machine Interface.',
    packages=find_packages(),
    install_requires=['click', 'flask'],
    tests_require=['pytest', 'pytest-cov'],
    entry_points='''
        [console_scripts]
        run_webserver=BaMMI.website:cli
        upload_thought=BaMMI.client:cli
        run_server=BaMMI.server:cli
    '''
)