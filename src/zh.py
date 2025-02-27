#!/usr/bin/env python3

# Copyright (c) 2017 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2017-12-15
#

"""zh [options] [<query>]

ZotHero - Alfred workflow for Zotero.

Usage:
    zh attachments <id> [<query>]
    zh citations <id> [<query>]
    zh clear
    zh config [<query>]
    zh copy [--bibliography] [--paste] <style> <id>
    zh copy [--paste] <citekey>
    zh fields [<query>]
    zh locale [<query>]
    zh notify [--title <msg>] [--text <msg>]
    zh reindex
    zh search <query>
    zh style [--style <key>] [<query>]
    zh setvar <key> <value>
    zh --help

Options:
    -b, --bibliography            Copy bibliography-style citation.
    -s <key>, --style=<key>       The currently-selected style.
    --title=<msg>                 Notification title.
    --text=<msg>                  Notification text.
    --paste                       Paste citation after copying it.
    -h, --help                    Show this message and exit.

"""

# from __future__ import print_function, absolute_import

import os
from operator import attrgetter
import sys
import json


sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from docopt import docopt
from workflow import Workflow3, ICON_WARNING, ICON_WEB
from workflow.background import is_running, run_in_background


log = None

# User's preferred citation style
CITE_STYLE = os.getenv('CITE_STYLE')
# User's preferred locale for citations
LOCALE = os.getenv('LOCALE')
COPY_CITEKEY_MOD = os.getenv('COPY_CITEKEY_MOD')



# Set if workflow was run via Snippet Trigger
AUTOPASTE = os.getenv('autopaste')

# GitHub repo to check for updates
UPDATE_SETTINGS = {
    'github_slug': 'deanishe/zothero',
    'prereleases': '-beta' in (os.getenv('alfred_workflow_version') or ''),
}

# URLs for help & docs
URL_ISSUES = 'https://github.com/giovannicoppola/zothero/issues'
URL_DOCS = 'https://github.com/deanishe/zothero/blob/master/README.md'

# Workflow icons
ICON_CITATION = 'icons/citation.png'
ICON_DOCS = 'icons/docs.png'
ICON_HELP = 'icons/help.png'
ICON_ISSUE = 'icons/issue.png'
ICON_LOCALE = 'icons/locale.png'
ICON_LOG = 'icons/log.png'
ICON_OFF = 'icons/off.png'
ICON_ON = 'icons/on.png'
ICON_RELOAD = 'icons/reload.png'
ICON_UPDATE_AVAILABLE = 'icons/update-available.png'
ICON_UPDATE_OK = 'icons/update-ok.png'


def do_fields(query):
    """View/filter available search fields."""
    from zothero.index import COLUMNS as cols
    if query:  # remove columns that don't start with `query`
        query = query.lower()
        cols = [col for col in cols if col.startswith(query)]

    for col in cols:
        wf.add_item(col.title(),
                    'Search in "{}"'.format(col),
                    arg=col + ':',
                    valid=True,
                    uid=col)

    wf.warn_empty('No matching columns', 'Try a different query?')
    wf.send_feedback()


def do_search(query):
    """Search the Zotero database."""
    from zothero import app
    from zothero.formatting import EntryFormatter
    from zothero.icons import entry_icon
    from zothero.index import COLUMNS


    
    style = None
    if CITE_STYLE:
        style = app.styles.get(CITE_STYLE)
        log.debug(u'Citation style: %s', style.name)

    # Add AUTOPASTE to workflow's variables, as Alfred's default
    # behaviour is to drop all other variables on the floor if
    # a modifier key is used.
    if AUTOPASTE:
        wf.setvar('autopaste', AUTOPASTE)

    # ------------------------------------------------------------------
    # Update index in background if it's out of date
    
    running = is_running('update')
    
    if app.stale and not running:
        run_in_background('update', [__file__, 'reindex'])
        log.debug('RUNNING BACKGROUND')
        running = True

    if running:  # Tell Alfred to re-run the workflow
        wf.rerun = 0.2

    # Get entries matching query
    entries = app.search(query)

    # ------------------------------------------------------------------
    # If no entries, show "Search XYZ" message or "no results" warning
    if not entries:
        if app.index.empty:  # no results because there's no search index
            wf.add_item(
                u'Initialising Search Index …',
                'Your results will appear momentarily',
                valid=False,
                icon=ICON_RELOAD,
            )

        elif query.endswith(':'):  # probably a category...
            col = query[:-1]
            if col in COLUMNS:
                wf.add_item(u'Search "{}"…'.format(col.title()))

        # Message wasn't added; show warning
        wf.warn_empty('No matches found', 'Try a different query?')

    # ------------------------------------------------------------------
    # Create and send Alfred feedback
    for i, e in enumerate(entries):
        #log.debug(u'%4d. %s', i + 1, e)
        f = EntryFormatter(e)
        sub = u'{} {}'.format(f.creators, f.year)
        key = u'{}_{}'.format(e.library, e.key)
        url = u'zotero://select/items/' + key
        if e.attachments:
            sub += u' Attachments: ' + str(len(e.attachments))

        if e.notes:
            large = u'\n\n'.join(e.notes)
        else:
            large = e.title or u'xxx'

        it = wf.add_item(e.title or u'xxx',
                         sub,
                         uid=e.id,
                         arg=e.id,
                         icon=entry_icon(e),
                         copytext=url,
                         largetext=large,
                         valid=True)

        it.setvar('action', 'open-in-zotero')
        it.setvar('url', url)
        it.setvar('citekey', e.citekey)
        it.setvar('id', e.id)

        # ------------------------------------------------------------------
        # Citations
        if style:
            it.setvar('stylename', style.name)  # for notification

            action = 'Paste' if AUTOPASTE else 'Copy'
            mod = it.add_modifier('cmd', u'%s citation (%s)' %
                                  (action, style.name))
            mod.setvar('action', 'copy-citation')
            mod.setvar('style', style.key)
            # For notification

            mod = it.add_modifier('alt', u'%s bibliography (%s)' %
                                  (action, style.name))
            mod.setvar('action', 'copy-citation')
            mod.setvar('bibliography', '1')
            mod.setvar('style', style.key)

        else:
            it.add_modifier('cmd', u'No citation format set', valid=False)
            it.add_modifier('alt', u'No citation format set', valid=False)

        # All citation formats
        mod = it.add_modifier('ctrl', 'View all citation formats')
        mod.setvar('action', 'show-citations')

        # Alternative open-in-zotero key with fn
        mod = it.add_modifier('fn', 'Open in Zotero')
        mod.setvar('action', 'open-in-zotero')
        mod.setvar('url', url)
        mod.setvar('id', e.id)

        # ------------------------------------------------------------------
        # Attachments
        if e.attachments:
            mod = it.add_modifier('shift', 'View attachments')
            mod.setvar('action', 'show-attachments')
        else:
            mod = it.add_modifier('shift', 'No attachments', valid=False)

        if e.citekey:
            
            
            # Override with copy-citekey action given COPY_CITEKEY_MOD
            if COPY_CITEKEY_MOD == '-':
                it.setvar('action', 'copy-citekey')
            elif COPY_CITEKEY_MOD in ['alt', 'cmd', 'ctrl', 'fn', 'shift']:
                action = 'Paste' if AUTOPASTE else 'Copy'
                mod = it.add_modifier(COPY_CITEKEY_MOD, action + u' cite-key')
                mod.setvar('action', 'copy-citekey')
            elif COPY_CITEKEY_MOD:
                log.warning('COPY_CITEKEY_MOD should be one of '
                            '-, alt, cmd, ctrl, fn, shift, or empty')

    wf.send_feedback()


def do_attachments(entry_id, query):
    """Filter and open an entry's attachments."""
    from zothero import app
    from zothero.util import shortpath

    e = app.entry(entry_id)

    if not e:
        wf.add_item('Unknown Entry', 'Entry was not found', icon=ICON_WARNING)
        wf.send_feedback()
        return

    if not e.attachments:
        wf.add_item('No Attachments', 'Entry has no attachments',
                    icon=ICON_WARNING)
        wf.send_feedback()
        return

    atts = e.attachments[:]
    if query:
        atts = wf.filter(query, atts, attrgetter('name'))

    for att in atts:
        if att.path:
            wf.add_item(att.name,
                        shortpath(att.path),
                        arg=att.path,
                        icon=att.path,
                        type='file',
                        icontype='fileicon',
                        valid=True)
        elif att.url:
            wf.add_item(att.name, att.url,
                        arg=att.url,
                        icon=ICON_WEB,
                        valid=True)

    wf.warn_empty('No Matching Attachments', 'Try a different query?')
    wf.send_feedback()


def do_citations(query, entry_id):
    """Filter citation formats."""
    from zothero import app

    # Get entry and styles
    e = app.entry(entry_id)
    if not e:
        raise ValueError('Unknown entry: ' + entry_id)

    styles = app.styles.all()

    # Filter styles
    if query:
        styles = wf.filter(query, styles, key=attrgetter('name'),
                           min_score=30)

    # Generate feedback
    action = 'Paste' if AUTOPASTE else 'Copy'
    for s in styles:
        it = wf.add_item(
            s.name,
            u'%s citation for "%s"' % (action, e.title),
            arg=s.key,
            icon=ICON_CITATION,
            valid=True,
        )
        it.setvar('id', entry_id)
        it.setvar('action', 'copy-citation')
        it.setvar('style', s.key)

        mod = it.add_modifier('cmd',
                              u'%s citation for “%s”' % (action, e.title))
        mod = it.add_modifier('alt',
                              u'%s bibliography for “%s”' % (action, e.title))
        mod.setvar('bibliography', '1')

        if s.key != CITE_STYLE:
            mod = it.add_modifier('ctrl', u'Set as default style')
            mod.setvar('varname', 'CITE_STYLE')
            mod.setvar('varval', s.key)
            mod.setvar('action', 'set-default')
            mod.setvar('next', 'citations')
            # For notification
            mod.setvar('notifytitle', 'Changed Default Style')
            mod.setvar('notifytext', s.name)
        else:
            mod = it.add_modifier('ctrl', u'This is the default style',
                                  valid=False)

    wf.warn_empty('No Matching Styles', 'Try a different query?')
    wf.send_feedback()


def do_copy(style_key, entry_id, bib_style=False, paste=False):
    """Copy a citation to the pasteboard."""
    from zothero import app
    #import pasteboard as pb

    wf.text_errors = True

    e = app.entry(entry_id)
    s = app.style(style_key)

    if not e:
        raise ValueError('Unknown Entry: %r' % entry_id)

    if not s:
        raise ValueError('Unknown Style: %r' % style_key)

    data = app.styles.cite(e, s, bib_style, LOCALE)

    ## Copying to clipboard
    # import subprocess
    # p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    # p.stdin.write(data['rtf'].encode())
    # p.stdin.close()
 
    # pbdata = {
    #     pb.UTI_HTML: data['html'],
    #     pb.UTI_PLAIN: data['text'],
    #     #log.debug ("RTF DATA %s" % str(data['rtf']))
    #     pb.UTI_TEXT: data['rtf'],
    # }
    # pb.set(pbdata)

        


    myVars = {}
    myVars ["alfredworkflow"] = {"variables": 
        {"UTI_HTML": data['html'],
        "UTI_PLAIN": data['text'],
        "UTI_RTF": data['rtf'],
        "autop2": "True"}
        }
     

    print (json.dumps(myVars))
    

    

    # if paste:
    #     from workflow.util import run_trigger
    #     run_trigger('paste')


def do_config(query):
    """Show workflow options."""
    from zothero import app
    from cite.locales import lookup

    style = None
    if CITE_STYLE:
        style = app.styles.get(CITE_STYLE)
        if not style:
            log.warning(u'Invalid style: %s', CITE_STYLE)
        else:
            log.debug(u'Default style: %s', style.name)

    items = []  # (item params, variables) tuples
    if wf.update_available:
        items.append((dict(
            title='An Update is Available',
            subtitle=u'↩ or ⇥ to install',
            autocomplete='workflow:update',
            valid=False,
            icon=ICON_UPDATE_AVAILABLE,
        ), {}))

    else:
        items.append((dict(
            title='Workflow is Up To Date',
            subtitle=u'↩ or ⇥ to force update check',
            autocomplete='workflow:update',
            valid=False,
            icon=ICON_UPDATE_OK,
        ), {}))

    # Style
    icon = ICON_OFF
    name = 'None'
    key = ''
    if style:
        icon = ICON_ON
        name = style.name
        key = style.key

    items.append((dict(
        title=u'Default Style: ' + name,
        subtitle=u'↩ to change style',
        valid=True,
        icon=icon,
    ), dict(
        action='choose-style',
        varname='CITE_STYLE',
        style=key,
    )))

    # Locale
    name = 'Default (US English)'
    icon = ICON_LOCALE
    if LOCALE:
        loc = lookup(LOCALE)
        if not loc:
            name = 'Invalid'
            icon = ICON_WARNING
        else:
            name = loc.name

    items.append((dict(
        title=u'Locale: ' + name,
        subtitle=u'↩ to change locale',
        valid=True,
        icon=icon,
    ), dict(
        action='choose-locale',
        varname='LOCALE',
    )))

    # Housekeeping
    items.append((dict(
        title='Reload Zotero Data',
        subtitle='Re-read your Zotero database',
        icon=ICON_RELOAD,
        valid=True,
    ), dict(
        action='reload',
    )))

    items.append((dict(
        title='Open Log File',
        subtitle='Open workflow log file in default app',
        autocomplete='workflow:openlog',
        icon=ICON_LOG,
        valid=False,
    ), {}))

    # Help
    items.append((dict(
        title='View Documentation',
        subtitle='Open the documentation in your browser',
        icon=ICON_DOCS,
        arg=URL_DOCS,
        valid=True,
    ), dict(
        action='open-url',
        url=URL_DOCS,
    )))

    items.append((dict(
        title='Report an Issue',
        subtitle='Open GitHub issue tracker in your browser',
        icon=ICON_ISSUE,
        arg=URL_ISSUES,
        valid=True,
    ), dict(
        action='open-url',
        url=URL_ISSUES,
    )))

    # ------------------------------------------------------------------
    # Filter and display items
    if query:
        items = wf.filter(query, items, key=lambda t: t[0]['title'],
                          min_score=30)

    for kwargs, variables in items:
        it = wf.add_item(**kwargs)
        for k, v in variables.items():
            it.setvar(k, v)

    wf.warn_empty('No Matching Options', 'Try a different query?')
    wf.send_feedback()


def do_style(query, style_key):
    """Choose a default style."""
    from zothero import app

    styles = app.styles.all()

    # Filter styles
    if query:
        styles = wf.filter(query, styles, key=attrgetter('name'),
                           min_score=30)

    for s in styles:
        icon = ICON_OFF
        valid = True
        sub = u'↩ to set as default style'
        if s.key == style_key:
            icon = ICON_ON
            valid = False
            sub = u'Current default style'

        it = wf.add_item(s.name,
                         sub,
                         valid=valid,
                         icon=icon)
        it.setvar('varval', s.key)
        # For notification
        # it.setvar('notifytitle', 'Changed Default Style')
        # it.setvar('notifytext', s.name)
        it.setvar('next', 'config')

    wf.warn_empty('No Matching Styles', 'Try a different query?')
    wf.send_feedback()


def do_locale(query):
    """Choose a locale."""
    from cite import locales

    locs = locales.all()

    # Filter styles
    if query:
        locs = wf.filter(query, locs, key=attrgetter('name'),
                         min_score=30)

    for l in locs:
        icon = ICON_OFF
        valid = True
        sub = u'↩ to set as locale'
        if l.code == LOCALE:
            icon = ICON_ON
            valid = False
            sub = u'Current locale'

        it = wf.add_item(l.name,
                         sub,
                         valid=valid,
                         icon=icon)
        it.setvar('varval', l.code)
        # For notification
        # it.setvar('notifytitle', 'Changed Locale')
        # it.setvar('notifytext', l.name)
        it.setvar('next', 'config')

    wf.warn_empty('No Matching Locales', 'Try a different query?')
    wf.send_feedback()


def do_clear():
    """Remove cached data."""
    from workflow import Variables

    def _deleteme(fn):
        x = os.path.splitext(fn)[1]
        return x.lower() in ('.sqlite', '.csl')

    wf.clear_cache(_deleteme)

    print(Variables(
        notifytitle=u'Cache Cleared',
        notifytext=u'Zotero database will be reloaded on next run',
    ))


def do_reindex():
    """Re-index search database.

    This command is called in a background job by `do_search()`.

    """
    from zothero import app
    # TODO: Decide whether to force a full update here.
    #
    # Only entries and attachments have a "modified" date.
    # If any entries or attachments have changed, only they
    # will be updated if force == False. Entries whose notes
    # have changed are not picked up.
    #
    # Changed notes are only be picked up if *no* entries
    # or attachments were changed (a full update is forced when
    # the library notices that the database has changed,
    # but there are no updated entries or attachments).
    #
    # Setting `force=True` reloads everything on every update.
    app.update_index(force=False)


def do_setvar(key, value):
    """Save a variable to ``info.plist``.

    Args:
        key (unicode): Name of variable to set.
        value (unicode): New value of variable.

    """
    from workflow.util import set_config
    log.debug('[settings] setting "%s" to "%s" ...', key, value)
    set_config(key, value, exportable=True)
    wf.send_feedback()


def do_notify(title, text):
    """Post a macOS notification.

    Does nothing if both ``title`` and ``text`` are empty.

    Args:
        title (unicode): Title for the notification.
        text (unicode): Text for the notification.

    """
    from workflow.notify import notify

    if not title and not text:
        log.debug('ignoring empty notification')
        return

    title = title or u'ZotHero'
    text = text or u''

    log.debug('[notification] title=%r, text=%r', title, text)
    notify(title, text)


def do_citekey(citekey, paste=False):
    """Copy Better Bibtext citekey.

    Args:
        citekey (unicode): Item's Better Bibtex citekey.
        paste (bool, optional): Paste citekey into active application.

    """
    log.debug('[citekey] key=%r, paste=%r', citekey, paste)
    from workflow.util import run_trigger
    import subprocess
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(citekey.encode())
    p.stdin.close()
 

    # if paste:
        
    #     run_trigger('paste')
        

def main(wf):
    """Run workflow."""
    import zothero

    wf.args  # call to ensure any magic arguments are intercepted
    args = docopt(__doc__, version=wf.version)
    # Ensure any string arguments are Unicode
    for k, v in args.items():
        if isinstance(v, str):
            args[k] = wf.decode(v)

    log.debug('args=%r', args)

    # Common parameters
    query = args.get('<query>')
    entry_id = int(args['<id>']) if args['<id>'] else None

    # Zotero data directories
    datadir = os.getenv('ZOTERO_DIR') or None
    attachdir = os.getenv('ATTACHMENTS_DIR') or None
    if datadir:
        datadir = wf.decode(os.path.expanduser(datadir))
    if attachdir:
        attachdir = wf.decode(os.path.expanduser(attachdir))

    app = zothero.ZotHero(wf.cachedir, datadir, attachdir)
    # Store app in `zothero` package where everything can access it.
    zothero.app = app

    if args['attachments']:
        return do_attachments(entry_id, query)

    if args['citations']:
        return do_citations(query, entry_id)

    if args['clear']:
        return do_clear()

    if args['config']:
        return do_config(args['<query>'])

    if args['copy']:
        if args['<citekey>']:
            return do_citekey(args['<citekey>'], args['--paste'])

        return do_copy(args['<style>'], entry_id, args['--bibliography'],
                       args['--paste'])

    if args['fields']:
        return do_fields(query)

    if args['locale']:
        return do_locale(query)

    if args['notify']:
        return do_notify(args['--title'], args['--text'])

    if args['reindex']:
        return do_reindex()

    if args['search']:
        return do_search(query)

    if args['style']:
        return do_style(query, args['--style'])

    if args['setvar']:
        return do_setvar(args['<key>'], args['<value>'])

    raise ValueError('Unknown command')


if __name__ == '__main__':
    wf = Workflow3(
        update_settings=UPDATE_SETTINGS,
        help_url=URL_ISSUES,
    )
    log = wf.logger
    wf.run(main)
