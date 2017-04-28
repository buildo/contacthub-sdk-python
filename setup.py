from setuptools import setup, find_packages

install_requires=[
    "configparser",
    'requests',
    'six'
]

testpkgs = [
    "nose==1.3.7",
    "coverage",
    "mock"
]
setup(description='ContactHub SDK Python',
      author='Axant',
      url='https://github.com/axant/contacthub-sdk-python',
      version='0.1',
      install_requires=install_requires,
      packages=find_packages(exclude=['tests', 'tests.*']),
      extras_require={
          'testing': testpkgs,
          'documentation': ['Sphinx==1.4.1', 'sphinx_rtd_theme']
      },
      scripts=[],
      name='contacthub',
      include_package_data=False,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=testpkgs,
      )
