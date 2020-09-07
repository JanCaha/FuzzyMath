# pylint: skip-file
from setuptools import setup, find_packages

setup(name='FuzzyMath',
      version='0.2.0',
      description='Small lightweight library for Python (version >= 3.6) '
                  'that performs basic Interval and Fuzzy Arithmetic.',
      url='https://github.com/JanCaha/FuzzyMath',
      author='Jan Caha',
      author_email='jan.caha@outlook.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['numpy'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
      )
