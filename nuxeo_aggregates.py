#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#
# Handles default configuration of aggregates for the Nuxeo repository

from messages_manager import Aggregate

NXAGGS = [
    Aggregate("target/messages.properties", [
            "nuxeo/nuxeo-features/nuxeo-platform-lang/src/main/resources/web/nuxeo.war/WEB-INF/classes/messages.properties",
            "nuxeo/nuxeo-features/nuxeo-platform-lang/src/main/resources/web/nuxeo.war/WEB-INF/classes/messages_en_US.properties",
            ]),
    Aggregate("target/messages_fr_FR.properties", [
            "nuxeo/nuxeo-features/nuxeo-platform-lang/src/main/resources/web/nuxeo.war/WEB-INF/classes/messages_fr_FR.properties",
            ]),
    ]

# add up all "external" languages
EXT_LANGUAGES = [
    "ar_SA",
    "ca_ES",
    "cs_CZ",
    "de_DE",
    "el_GR",
    "es_ES",
    "eu_ES",
    "fr_CA",
    "gl_ES",
    "it_IT",
    "ja_JP",
    "mk_MK",
    "nl_NL",
    "pl_PL",
    "pt_BR",
    "pt_PT",
    "ru_RU",
    "sr_RS",
    "tr_TR",
    "vi_VN",
    "zh_CN",
]

for lang in EXT_LANGUAGES:
    NXAGGS.append(
        Aggregate("target/messages/%s.properties" % (lang,), [
                "nuxeo/addons/nuxeo-platform-lang-ext/src/main/resources/web/nuxeo.war/WEB-INF/classes/messages_%s.properties" % (lang,),
                ]))
