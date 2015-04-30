# Nuxeo Crowdin Integration

This module holds helper bash and python scripts to handle
synchronization of translation files from/to Crowdin.

The python scripts are useful to aggregate and split contributions (as
the en_US and fr_FR translation files are split accross different
Nuxeo bundles).

The bash scripts are useful to call python scripts (and other helpers)
that will:
- push changes from Crowdin to Nuxeo
- push changes from Nuxeo to Crowdin

# Nuxeo default modules and main addons management

### Adding/Removing an addon translation files from the Crowdin main file

Only one file is maintained on Crowdin side for translation management.

Translation files for Nuxeo default addons are kept in file
nuxeo_aggregates.py.

When adding/removing Nuxeo modules that contribute to the Crowdin
files, the nuxeo_aggregates.py file configuration should be updated.

A Jenkins job can be setup to call script at
jenkins/push_to_crowdin.sh to handle changes to this file. It accepts
options to push only English and French translation files, or all the
other languages maintained as one big file in the
nuxeo-platform-lang-ext module. It is supposed to be added to the
continuous intgeration of the project, for the master branch (only
this branch is handled via Crowdin).

Another Jenkins job can be setup to call script at
jenkins/push_to_nuxeo.sh to handle changes the other way around. This
change is supposed to be triggered manually after an update on Crowdin
side (also to avoid roundtrip changes in case of small variations in
translation files content).

As a general rule: github is the master reference version, and changes
on Crowdin side should be reported to github *before* an automatic
push from Nuxeo to Crowdin, otherwise they could be lost.

Check the scripts documentation for more information about available
options.

### Adding/removing a language to the translation files from/to Crowdin


TODO: decide the push/pull policy for new languages since the
deployment-fragment file needs to be updated too.

+ check what kind of syncs should be done in what direction


# Nuxeo additional plugins use case

This module methods can be reused to generate a configuration specific
to your project, taking example on script nuxeo_aggregates.py.

Similar bash scripts can be setup for an integration with any other
Crowdin project.

# About Nuxeo

Nuxeo dramatically improves how content-based applications are built, managed and deployed, making customers more agile, innovative and successful. Nuxeo provides a next generation, enterprise ready platform for building traditional and cutting-edge content oriented applications. Combining a powerful application development environment with SaaS-based tools and a modular architecture, the Nuxeo Platform and Products provide clear business value to some of the most recognizable brands including Verizon, Electronic Arts, Netflix, Sharp, FICO, the U.S. Navy, and Boeing. Nuxeo is headquartered in New York and Paris. More information is available at [www.nuxeo.com](http://www.nuxeo.com).
