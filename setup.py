from setuptools import setup, find_packages
from os import path

setup_file_location = path.abspath(path.dirname(__file__))
with open(path.join(setup_file_location, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pigeon-cli',
    version='0.0.3',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/LiamDoult/python-template',
    author='Liam Doult',
    author_email='liam.doult@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='template repository development',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, < 4',
    install_requires=[
        'click',
        'requests',
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': [],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/LiamDoult/pigeon-cli/issues',
        'Source': 'https://github.com/LiamDoult/pigeon-cli/',
    },
)
