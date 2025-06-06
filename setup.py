from setuptools import setup, find_packages

setup(
    name="ibmsecurity",
    packages=find_packages(),
    # Date of release used for version - please be sure to use YYYY.MM.DD.seq#, MM and DD should be two digits e.g. 2017.02.05.0
    # seq# will be zero unless there are multiple release on a given day - then increment by one for additional release for that date
    version="2025.6.3.0",
    description="Idempotent functions for IBM Security Appliance REST APIs",
    author="IBM",
    author_email="secorch@wwpdl.vnet.ibm.com",
    url="",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Build Tools",
    ],
    zip_safe=False,
    install_requires=["requests", "jmespath"],
)
