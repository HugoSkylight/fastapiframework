from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="fast-rest-framework",
    version="0.0.1",
    author="Whliao",
    url="https://github.com/Oceans594/fastapiframework",
    install_requires=[],
    license='BSD License',
    description="A fastapi framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ]
)