from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'Hearts library',
  ext_modules = cythonize("hearts.pyx"),
)
