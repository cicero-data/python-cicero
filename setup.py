from setuptools import setup, find_packages

setup(
    name='python-cicero',
    version='0.1.0',
    author='Azavea',
    author_email='info@azavea.com',
    maintainer='Andrew Thompson',
    maintainer_email='athompson@azavea.com',
    packages=find_packages(),
    url=['http://github.com/azavea/python-cicero'],
    license='LICENSE.txt',
    description='Python wrapper for Azavea\'s Cicero API',
    long_description=open('README.rst').read(),
    install_requires=[],
    extras_require = { 'docs': ["pycco"],},
    test_suite = "cicero.test.tests",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: GIS',
        'Programming Language :: Python :: 2.7'
    ],
)
