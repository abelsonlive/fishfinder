from setuptools import setup, find_packages
import os 
from pip.req import parse_requirements

# hack for working with pandocs
import codecs 
try: 
  codecs.lookup('mbcs') 
except LookupError: 
  utf8 = codecs.lookup('utf-8') 
  func = lambda name, enc=utf8: {True: enc}.get(name=='mbcs') 
  codecs.register(func) 

# install readme
# readme = os.path.join(os.path.dirname(__file__), 'README.md')

# setup
setup(
  name='fishfinder',
  version='0.0.3',
  description='recursively search all possibilities until the optimal set is found',
  long_description = '',
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    ],
  keywords='',
  author='Brian Abelson',
  author_email='brianabelson@gmail.com',
  url='http://github.com/abelsonlive/fishfinder',
  license='MIT',
  packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
  namespace_packages=[],
  include_package_data=False,
  zip_safe=False,
  install_requires=[
    'gevent'
  ],
  tests_require=[]
)