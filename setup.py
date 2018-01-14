from setuptools import setup, find_packages

setup(
    name = 'ibmsecurity',
    packages = find_packages(),
    # Date of release used for version - please be sure to use YYYY.MM.DD.seq#, MM and DD should be two digits e.g. 2017.02.05.0
    version = '2018.01.10.0',
    description = 'Idempotent functions for IBM Security Appliance REST APIs',
    author='IBM',
    author_email='ISAMDEV@au1.ibm.com',
    url='',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: IBM :: Apache',
        'Operating System :: OS Independent',
        'Development Status :: GA',
        'Environment :: Console',
        'Intended Audience :: IBM Security Appliance Users',
        'Topic :: IBM:: Security'
    ],
    zip_safe = False,
    install_requires = [
        'importlib',
        'requests'
    ]
)
