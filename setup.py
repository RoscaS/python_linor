from setuptools import find_packages
from setuptools import setup


setup(
    name='Linor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "numpy == 1.18.4",
        "opencv-contrib-python == 4.2.0.34",
        "pywin32 == 227",
    ]
)
