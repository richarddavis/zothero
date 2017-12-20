# encoding: utf-8
#
# Copyright (c) 2017 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2017-12-15
#

"""Core classes and functions representing the main zothero API."""

from __future__ import print_function, absolute_import

import logging
import os

from .util import copyifnewer, unicodify, shortpath

# Default location of Zotero's data in version 5
DEFAULT_ZOTERO_DIR = '~/Zotero'

log = logging.getLogger(__name__)


class ZotHero(object):
    """Main workflow application object.

    Attributes:
        wf (workflow.Workflow3): The active `Workflow3` object for this
            workflow.
    """

    def __init__(self, cachedir):
        """Create new `ZotHero` using ``cachedir``."""
        log.debug('[core] cachedir=%r', shortpath(cachedir))
        self.cachedir = cachedir

        # Copy of Zotero database. Zotero locks the original, so
        # it's necessary to make a copy
        self._copy_path = os.path.join(cachedir, 'zotero.sqlite')

        # Attributes to back lazy-loading properties
        self._zotero_dir = None  # Zotero's data directory
        self._zot = None  # Zotero object
        self._cache = None  # Cache object
        self._index = None  # Index object
        self._styles = None  # Styles object

    @property
    def zotero_dir(self):
        """Path to Zotero's data folder.

        This is the folder where ``zotero.sqlite``, ``storage`` and
        ``styles`` are located.

        Read from the ``ZOTERO_DIR`` environment/workflow variable.
        If unset, the default of ``~/Zotero`` is used.

        """
        if not self._zotero_dir:
            path = os.path.expanduser(os.getenv('ZOTERO_DIR') or
                                      DEFAULT_ZOTERO_DIR)
            if not os.path.exists(path):
                raise ValueError('Zotero directory does not exist: %r' % path)

            self._zotero_dir = unicodify(path)

        return self._zotero_dir

    @property
    def zotero(self):
        """Zotero instance.

        Initialses and returns a `zothero.zotero.Zotero` instance
        based on :attr:`zotero_path`.

        Returns:
            zothero.zotero.Zotero: Initialised `Zotero` object.
        """
        from .zotero import Zotero

        if not self._zot:
            original = os.path.join(self.zotero_dir, 'zotero.sqlite')
            if not os.path.exists(original):
                raise ValueError('Zotero database not found: %r' % original)

            # Ensure cached copy of database is up to date
            dbpath = copyifnewer(original, self._copy_path)

            self._zot = Zotero(self.zotero_dir, dbpath)

            # Validate paths by calling storage & styles properties
            log.debug('[core] storage=%r', shortpath(self._zot.storage_dir))
            log.debug('[core] styles=%r', shortpath(self._zot.styles_dir))

        return self._zot

    @property
    def index(self):
        """Search index.

        Creates and returns an `Index`. May be empty.

        Returns:
            zothero.index.Index: Initialised search index.
        """
        if not self._index:
            from .index import Index
            self._index = Index(os.path.join(self.cachedir, 'search.sqlite'))
            self._index.update(self.zotero)

        return self._index

    @property
    def cache(self):
        """Top-level cache."""
        if not self._cache:
            from .cache import Cache
            self._cache = Cache(os.path.join(self.cachedir, 'cache.sqlite'))

        return self._cache

    @property
    def styles(self):
        """CSL Styles loader."""
        if not self._styles:
            from .styles import Styles
            self._styles = Styles(self.zotero.styles_dir, self.cache)

        return self._styles

    def entry(self, key):
        """Retrieve `Entry` for ``key``.

        Args:
            key (str): Zotero database key

        Returns:
            zothero.zotero.Entry: `Entry` for `key` or `None` if not found.
        """
        return self.index.entry(key)

    def search(self, query):
        """Search the Zotero database."""
        log.info(u'[core] searching for "%s" ...', query)
        return self.index.search(query)

    def style(self, key):
        """Return CSL style for key."""
        return self.styles.get(key)
