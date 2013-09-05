from setuptools import setup


setup(
    name='roc',
    version='1.0',
    package_dir={'roc': 'src'},
    packages=['roc'],
    description=open('readme.md', 'rt').read(),
    author='Peter Demin',
    author_email='poslano@gmail.com',
    test_suite='tests.tests',
    install_requires=(
         'setuptools>=0.6b1',
         'six',
    ),
)
