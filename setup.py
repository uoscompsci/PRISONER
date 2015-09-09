from setuptools import setup

setup(name='PRISONER',
      version='0.2.4',
      description="Framework for ethical and reproducible social network\
      experiments",
      long_description="",
      author='Luke Hutton',
      author_email='lh49@st-andrews.ac.uk',
      license='BSD',
      packages=['gateway','persistence','server','tests','tools','workflow'],
      zip_safe=False,
      install_requires=[
          ],
      )