from setuptools import setup


setup(
    name='roc',
    version='0.1.2',
    package_dir={'roc': 'roc'},
    packages=['roc'],
    description=open('readme.md', 'rt').read(),
    author='Peter Demin',
    author_email='poslano@gmail.com',
    install_requires=(
         'setuptools>=0.6b1',
         'six',
    ),
)
