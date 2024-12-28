from setuptools import setup, find_packages

setup(
    name="py-life-360",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # List your dependencies here
    description="A package for interfacing with Life360",
    author="Sam Ramirez",
    url="https://github.com/arkangel-dev/py-life-360",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.6",
)