#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Handles default configuration of aggregates for the Nuxeo default modules and main addons.

Usage: ./nuxeo_aggregates.py [options] targetdir

Options:
    -h / --help
        Print this message and exit.

    --a
        Handle all languages (fr, en + ext)
    --e
        Only handle ext languages (default: handle only fr and en messages)
"""

import sys, getopt, argparse
from messages_manager import Aggregate, MessagesManager

# translations for all default modules/addons that should be maintained with the help of Crowdin
NXAGGS = [
    Aggregate("messages.properties", [
            "nuxeo/nuxeo-features/nuxeo-platform-lang/src/main/resources/web/nuxeo.war/WEB-INF/classes/messages_en_US.properties",
            "nuxeo/nuxeo-features/nuxeo-platform-collections/nuxeo-platform-collections-jsf/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/nuxeo-features/nuxeo-search-ui/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/nuxeo-features/nuxeo-platform-rendition/nuxeo-platform-rendition-publisher/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/nuxeo-features/nuxeo-platform-rendition/nuxeo-platform-rendition-web/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-groups-rights-audit/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-tree-snapshot/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-login/nuxeo-platform-login-shibboleth/src/main/resources/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-login/nuxeo-platform-login-deputy/src/main/resources/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-login/nuxeo-platform-login-token/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-imaging-recompute/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-multi-tenant/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-logs-viewer/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-rating/nuxeo-rating-web/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-user-registration/nuxeo-platform-user-registration-web/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-agenda/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-diff/nuxeo-diff-jsf/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-signature/nuxeo-platform-signature-web/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-user-center/nuxeo-user-profile/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-user-center/nuxeo-user-dashboard/nuxeo-user-dashboard/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-user-center/nuxeo-user-center/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-user-center/nuxeo-user-oauth/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-user-center/nuxeo-user-notification/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-suggestbox/nuxeo-platform-suggestbox-jsf/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-spreadsheet/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-document-routing/nuxeo-routing-web/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-document-routing/nuxeo-routing-dm/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-document-routing/nuxeo-routing-dashboard/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-document-routing/nuxeo-routing-default/src/main/resources/data/i18n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-video/nuxeo-platform-video-jsf/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-quota/nuxeo-quota-web/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-csv/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-template-rendering/nuxeo-template-rendering-samples/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-template-rendering/nuxeo-template-rendering-web/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-webengine-sites/nuxeo-webengine-blogs/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-webengine-sites/nuxeo-webengine-sites/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-birt/nuxeo-birt-reporting-web/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-drive-server/nuxeo-drive-jsf/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            "nuxeo/addons/nuxeo-platform-audio/nuxeo-platform-audio-jsf/src/main/resources/OSGI-INF/l10n/messages_en_US.properties",
            ]),
    Aggregate("fr/messages_fr_FR.properties", [
            "nuxeo/nuxeo-features/nuxeo-platform-lang/src/main/resources/web/nuxeo.war/WEB-INF/classes/messages_fr_FR.properties",
            "nuxeo/nuxeo-features/nuxeo-platform-collections/nuxeo-platform-collections-jsf/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/nuxeo-features/nuxeo-search-ui/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/nuxeo-features/nuxeo-platform-rendition/nuxeo-platform-rendition-publisher/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/nuxeo-features/nuxeo-platform-rendition/nuxeo-platform-rendition-web/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-groups-rights-audit/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-tree-snapshot/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-login/nuxeo-platform-login-shibboleth/src/main/resources/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-login/nuxeo-platform-login-deputy/src/main/resources/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-login/nuxeo-platform-login-token/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-imaging-recompute/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-multi-tenant/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-logs-viewer/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-rating/nuxeo-rating-web/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-user-registration/nuxeo-platform-user-registration-web/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-agenda/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-diff/nuxeo-diff-jsf/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-signature/nuxeo-platform-signature-web/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-user-center/nuxeo-user-profile/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-user-center/nuxeo-user-dashboard/nuxeo-user-dashboard/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-user-center/nuxeo-user-center/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-user-center/nuxeo-user-oauth/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-user-center/nuxeo-user-notification/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-suggestbox/nuxeo-platform-suggestbox-jsf/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-spreadsheet/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-document-routing/nuxeo-routing-web/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-document-routing/nuxeo-routing-dm/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-document-routing/nuxeo-routing-dashboard/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-document-routing/nuxeo-routing-default/src/main/resources/data/i18n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-video/nuxeo-platform-video-jsf/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-quota/nuxeo-quota-web/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-csv/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-template-rendering/nuxeo-template-rendering-samples/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-template-rendering/nuxeo-template-rendering-web/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-webengine-sites/nuxeo-webengine-blogs/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-webengine-sites/nuxeo-webengine-sites/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-birt/nuxeo-birt-reporting-web/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-drive-server/nuxeo-drive-jsf/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            "nuxeo/addons/nuxeo-platform-audio/nuxeo-platform-audio-jsf/src/main/resources/OSGI-INF/l10n/messages_fr_FR.properties",
            ]),
    ]

# add up all "external" languages, where only one file is maintained
# anyway, to be maintained accordingly to languages in
# nuxeo-platform-lang-ext module (and declared in its
# deployment-fragment file)
EXT_LANGUAGES = [
    ("ar", "ar_SA"),
    ("ca", "ca_ES"),
    ("cs", "cs_CZ"),
    ("de", "de_DE"),
    ("el", "el_GR"),
    ("es_ES", "es_ES"),
    ("eu", "eu_ES"),
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

NXAGGS_EXT = []
for lang in EXT_LANGUAGES:
    NXAGGS_EXT.append(
        Aggregate("%s/messages_%s.properties" % (lang[0], lang[1],), [
                "nuxeo/addons/nuxeo-platform-lang-ext/src/main/resources/web/nuxeo.war/WEB-INF/classes/messages_%s.properties" % (lang[1],),
                ]))

NXAGGS_ALL = []
NXAGGS_ALL.extend(NXAGGS)
NXAGGS_ALL.extend(NXAGGS_EXT)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('outputdir', help='the output directory (mandatory)')
    parser.add_argument('--a', dest='all', action='store_true')
    parser.add_argument('--ext', dest='ext', action='store_true')
    args = parser.parse_args()

    aggs = NXAGGS
    if args.ext is True:
        aggs = NXAGGS_EXT
    if args.all is True:
        aggs = NXAGGS_ALL

    MessagesManager(aggs).aggregate(args.outputdir);

if __name__ == '__main__':
    main()
