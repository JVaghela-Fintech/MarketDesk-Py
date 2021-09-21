from setuptools import setup

setup(
    name='marketdesk',
    version='0.0.1',
    description='socket library to connect the marketdesk real-time fx feed',
    long_description='socket library to connect the marketdesk real-time fx feed',
    author='FintechGlobalCenter',
    author_email='ops@fintechglobal.center',
    packages=['marketdesk'],
#   no dependencies in this example
    install_requires=[
        'websocket',
    ],
    python_requires = '>=2.7',
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'],
    )
