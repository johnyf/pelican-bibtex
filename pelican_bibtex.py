"""
Pelican BibTeX
==============

A Pelican plugin that populates the context with a list of formatted
citations, loaded from a BibTeX file at a configurable path.

The use case for now is to generate a ``Publications'' page for academic
websites.
"""
# Author: Vlad Niculae <vlad@vene.ro>
# Unlicense (see UNLICENSE for details)

import logging
import re
logger = logging.getLogger(__name__)

from pelican import signals

__version__ = '0.2.1'


def add_publications(generator):
    """
    Populates context with a list of BibTeX publications.

    Configuration
    -------------
    generator.settings['PUBLICATIONS_SRC']:
        local path to the BibTeX file to read.

    Output
    ------
    generator.context['publications']:
        List of tuples (key, year, text, bibtex, pdf, slides, poster).
        See Readme.md for more details.
    """
    if 'PUBLICATIONS_SRC' not in generator.settings:
        return
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
    try:
        from pybtex.database.input.bibtex import Parser
        from pybtex.database.output.bibtex import Writer
        from pybtex.database import BibliographyData, PybtexError
        from pybtex.backends import html
        from pybtex.style.formatting import plain
        from pybtex import richtext
    except ImportError:
        logger.warn('`pelican_bibtex` failed to load dependency `pybtex`')
        return

    refs_file = generator.settings['PUBLICATIONS_SRC']
    try:
        bibdata_all = Parser().parse_file(refs_file)
    except PybtexError as e:
        logger.warn('`pelican_bibtex` failed to parse file %s: %s' % (
            refs_file,
            str(e)))
        return

    publications = []

    # format entries
    plain_style = plain.Style()
    html_backend = html.Backend()
    formatted_entries = plain_style.format_entries(bibdata_all.entries.values())

    def filter_str(s):
        if not isinstance(s, richtext.String):
            return s
        s.value = re.sub(r'(?<!\\)}', '', s.value)
        s.value = re.sub(r'(?<!\\){', '', s.value)
        return s

    for formatted_entry in formatted_entries:
        formatted_entry.text.parts = [filter_str(s) for s in formatted_entry.text.parts]
        key = formatted_entry.key
        entry = bibdata_all.entries[key]
        year = entry.fields.get('year')
        # This shouldn't really stay in the field dict
        # but new versions of pybtex don't support pop
        pdf = entry.fields.get('pdf', None)
        slides = entry.fields.get('slides', None)
        poster = entry.fields.get('poster', None)
        code = entry.fields.get('code', None)
        session = entry.fields.get('session', None)
        index = entry.fields.get('index', None)
        school = entry.fields.get('school', None)
        index = int(index)
        type_ = entry.type

        #render the bibtex string for the entry
        bib_buf = StringIO()
        bibdata_this = BibliographyData(entries={key: entry})
        Writer().write_stream(bibdata_this, bib_buf)
        text = formatted_entry.text.render(html_backend)
        
        # TODO: use dict of dicts
        publications.append((key,
                             index,
                             year,
                             text,
                             bib_buf.getvalue(),
                             pdf,
                             slides,
                             poster,
                             code,
                             type_,
                             session,
                             school))
    # sort by date
    publications = [pub for pub in sorted(publications,
        key=lambda x: x[1], reverse=True)]
    for p in publications:
        print((p[:2]))

    generator.context['publications'] = publications


def register():
    signals.generator_init.connect(add_publications)
