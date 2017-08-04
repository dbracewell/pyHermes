from setuptools import setup
from Cython.Build import cythonize

setup(name="pyHermes",
      packages=["."],
      install_requires=['quicksect', 'spacy', 'nltk', 'jieba', 'regex'],
      ext_modules=cythonize('hermes/util/interval.pyx')
      )
