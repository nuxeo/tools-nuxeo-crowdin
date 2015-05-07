# Nuxeo Crowdin Integration

This module holds helper bash and python scripts to handle
synchronization of translation files from/to Crowdin.

The python scripts are useful to aggregate and split contributions (as
the en_US translation files are split accross different Nuxeo
bundles).

The bash scripts are useful to call python scripts (and other helpers)
that will:
- push changes from Crowdin to Nuxeo
- push changes from Nuxeo to Crowdin

# Nuxeo default modules and main addons management

### Adding/Removing an addon translation files from the Crowdin main file

Only one file is maintained on Crowdin side for translation management.

Nuxeo modules that should contribute to the Crowdin files should hold
a root crowdin.ini file, specifying the properties file path.

A Jenkins job can be setup to call script at
jenkins/sync_nuxeo_crowdin.sh to handle changes to this file. It
accepts options to push only the English reference translation file,
managed as one big file in the nuxeo-platform-lang-ext module. Only
the master branch is handled via Crowdin.

The same Jenkins job can be configured to trigger update of ext
languages files from Crowdin, to handle changes the other way
around. This change is supposed to be triggered by a timer, or
manually, after an update on Crowdin side.

As a general rule: github is the master reference version, and changes
on Crowdin side should be reported to github *before* an automatic
push from Nuxeo to Crowdin, otherwise they could be lost.

Check the scripts documentation for more information about available
options.

# Nuxeo additional plugins use case

This module methods can be reused to generate a configuration specific
to your project, taking example on script nuxeo_aggregates.py.

Similar bash scripts can be setup for an integration with any other
Crowdin project.

# About Nuxeo

Nuxeo dramatically improves how content-based applications are built, managed and deployed, making customers more agile, innovative and successful. Nuxeo provides a next generation, enterprise ready platform for building traditional and cutting-edge content oriented applications. Combining a powerful application development environment with SaaS-based tools and a modular architecture, the Nuxeo Platform and Products provide clear business value to some of the most recognizable brands including Verizon, Electronic Arts, Netflix, Sharp, FICO, the U.S. Navy, and Boeing. Nuxeo is headquartered in New York and Paris. More information is available at [www.nuxeo.com](http://www.nuxeo.com).
