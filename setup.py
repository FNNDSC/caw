from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.md')) as f:
    readme = f.read()

# noinspection PyPackageRequirements
setup(
    name='caw',
    version='0.1.0',
    packages=['caw', 'chrisclient2'],
    url='https://github.com/FNNDSC/caw',
    license='MIT',
    author='Jennings Zhang',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    description='ChRIS Automatic Workflows',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    install_requires=['requests', 'typer', 'shellingham'],
    entry_points={
        'console_scripts': [
            'caw = caw.__main__:app'
            ]
        },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)

