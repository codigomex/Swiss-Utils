from setuptools import find_packages, setup

setup(
    name='pyutils',
    version='0.1.0',
    author='Your Name',
    description='Essential Python utilities for console, math, system, and more',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.8',
    license='MIT',
)
