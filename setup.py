import pelican_bibtex
from setuptools import setup

CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: Public Domain
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Software Development
Operating System :: POSIX
Operating System :: Unix

"""

LONG_DESCRIPTION = """\
Requirements
============

pelican\_bibtex requires pybtex.

This plugin reads a user-specified BibTeX file and populates the context with
a list of publications, ready to be used in your Jinja2 template.

If the file is present and readable, you will be able to find the 'publications'
variable in all templates.  It is a list of tuples with the following fields:
(key, text, bibtex, pdf, slides, poster)

1. key is the BibTeX key (identifier) of the entry.
2. text is the HTML formatted entry, generated by pybtex.
3. bibtex is a string containing BibTeX code for the entry, useful to make it
   available to people who want to cite your work.
4. pdf, slides, poster: in your BibTeX file, you can add these special fields

"""

setup(
    name='pelican_bibtex',
    description='Organize your scientific publications with BibTeX in Pelican',
    long_description=LONG_DESCRIPTION,
    version=pelican_bibtex.__version__,
    author='Vlad Niculae',
    author_email='vlad@vene.ro',
    url='https://pypi.python.org/pypi/pelican_bibtex',
    py_modules=['pelican_bibtex'],
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f]
)
