from os import path
from setuptools import setup, find_packages

with open(path.join(path.dirname(path.abspath(__file__)), 'README.md')) as f:
    readme = f.read()

setup(
    name='caw',
    version='0.7.0',
    packages=find_packages(exclude=('*.tests',)),
    url='https://github.com/FNNDSC/caw',
    license='MIT',
    author='Jennings Zhang',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    description='ChRIS client',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.8.2',
    install_requires=['requests', 'typer'],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)
