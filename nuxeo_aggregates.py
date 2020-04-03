#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Handles default configuration of aggregates for the Nuxeo default modules and main addons.

Usage: ./nuxeo_aggregates.py [options] inputdir outputdir

Options:
    -h / --help
        Print this message and exit.

    --a
        Handle all languages (en + ext)
    --e
        Only handle ext languages (default: handle only en messages)
"""

import sys, os, argparse
from messages_manager import Aggregate, AggregatesParser, MessagesManager

MAIN_LANG_MODULE_PATH = 'modules/platform/nuxeo-platform-lang'
EXT_LANG_MODULE_PATH = 'modules/platform/nuxeo-platform-lang-ext'

DEFAULT_LANGS = {
    "en_US": ("messages.properties", ""),
}

EXT_LANGS = {}
EXT_LANGUAGES = [
    ("ar", "ar_SA"),
    ("ca", "ca_ES"),
    ("cs", "cs_CZ"),
    ("de", "de_DE"),
    ("el", "el_GR"),
    ("es_ES", "es_ES"),
    ("eu", "eu_ES"),
    ("fr", "fr_FR"),
    ("fr_CA", "fr_CA"),
    ("gl", "gl_ES"),
    ("it", "it_IT"),
    ("ja", "ja_JP"),
    ("mk", "mk_MK"),
    ("nl", "nl_NL"),
    ("pl", "pl_PL"),
    ("pt_BR", "pt_BR"),
    ("pt_PT", "pt_PT"),
    ("ru", "ru_RU"),
    ("sr", "sr_RS"),
    ("tr", "tr_TR"),
    ("vi", "vi_VN"),
    ("zh_CN", "zh_CN"),
]
for lang in EXT_LANGUAGES:
    EXT_LANGS[lang[1]] = ("messages_%s.properties" %(lang[1],), lang[0])

ALL_LANGS = {}
ALL_LANGS.update(DEFAULT_LANGS)
ALL_LANGS.update(EXT_LANGS)

def aggregate(inputdir, outputdir, ext=False, all=False):
    ap = AggregatesParser()

    # make sure platform-lang is the first one on the sorted list of results
    main_res = ap.load(os.path.join(inputdir, MAIN_LANG_MODULE_PATH), 'nuxeo')
    ext_res = ap.load(inputdir, 'nuxeo', excluded_dirs=[MAIN_LANG_MODULE_PATH])

    langs = DEFAULT_LANGS
    if all is True:
        langs = ALL_LANGS
    elif ext is True:
        langs = EXT_LANGS

    aggs = []
    for lang in langs:
        lang_paths = []
        if lang in main_res:
            lang_paths.extend(main_res[lang])
        if lang in ext_res:
            ext_paths = ext_res[lang]
            ext_paths.sort()
            lang_paths.extend(ext_paths)
        if len(lang_paths) > 0:
            lang_vals = langs[lang]
            aggs.append(Aggregate(os.path.join(lang_vals[1], lang_vals[0]), lang_paths))

    MessagesManager(aggs).aggregate(outputdir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', help='the input directory (mandatory)')
    parser.add_argument('outputdir', help='the output directory (mandatory)')
    parser.add_argument('--a', dest='all', action='store_true')
    parser.add_argument('--ext', dest='ext', action='store_true')
    args = parser.parse_args()
    aggregate(args.inputdir, args.outputdir, ext=args.ext, all=args.all)

if __name__ == '__main__':
    main()
