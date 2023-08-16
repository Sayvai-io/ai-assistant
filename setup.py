from setuptools import setup, find_packages
from src.kutty import __version__

core_requirements = [
    'langchain',
    'llama_index',
]

setup(
    name='kutty',
    version=__version__,
    description='A Python package for generating a server that can be used to schedule meetings',
    author='sayvai-io',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=core_requirements,
    extras_require={
        'dev': [
            'pytest',
            'pylint',
        ],
    },
    zip_safe=False
)
    