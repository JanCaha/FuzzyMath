# pylint: skip-file
from setuptools import setup, find_packages
import unittest


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(name='FuzzyMath',
      version='0.3.0',
      description='Small lightweight library for Python (version >= 3.6) '
                  'that performs basic Interval and Fuzzy Arithmetic.',
      url='https://github.com/JanCaha/FuzzyMath',
      author='Jan Caha',
      author_email='jan.caha@outlook.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['numpy'],
      zip_safe=False,
      test_suite='setup.my_test_suite'
      )
