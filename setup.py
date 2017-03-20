from setuptools import setup, find_packages
 
setup(
    name = 'ibmsecurity',
    packages = find_packages(),
    version = '2017.03.20.0',
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
