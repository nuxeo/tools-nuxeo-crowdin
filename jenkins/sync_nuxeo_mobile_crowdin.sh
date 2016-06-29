#!/bin/bash -xe
# Bash script for jenkins, expected to be executed from a workspace
# with the following structure:
# - nuxeo-mobile
# - tools-nuxeo-crowdin
#
# Directory "nuxeo-mobile" is a checkout of the nuxeo-mobile repository.
#
# The nuxeo-mobile/src/i18n directory is changed by this script.
#
# Parameters:
# - PROJECT: Crowdin project name (nuxeo-mobile by default)
# - FORMAT: Crowdin project format (json by default)
# - KEY: Crowdin project API key
# - BRANCH: Nuxeo Mobile branch to work (master by default, see commons.sh)
# - COMMIT_BRANCH: if not blank, branch to work on, created from $BRANCH
# - JIRA: if not blank, jira issue to reference on commit message
#
# Boolean params for corresponding actions:
# - UPDATE_CROWDIN_FROM_NUXEO (default to false if var unset)
# - UPDATE_NUXEO_FROM_CROWDIN (default to false if var unset)
# - DRYRUN: if set to true, changes will not be pushed to GitHub and
#   Crowdin (default to true if var unset, see commons.sh)

set -e

HERE=`pwd`
SCRIPT_PATH="`dirname \"$0\"`"
NUXEO_MOBILE_PATH=./nuxeo-mobile

# Include common variables and functions
source $SCRIPT_PATH/common.sh

#
# Init parameters
#
if [ -z ${PROJECT+x} ]; then
    PROJECT="nuxeo-mobile"
fi
if [ -z ${FORMAT+x} ]; then
    FORMAT="json"
fi
if [ -z ${UPDATE_CROWDIN_FROM_NUXEO+x} ]; then
    UPDATE_CROWDIN_FROM_NUXEO=false
fi
if [ -z ${UPDATE_NUXEO_FROM_CROWDIN+x} ]; then
    UPDATE_NUXEO_FROM_CROWDIN=false
fi

#
# Nuxeo Mobile -> Crowdin update
#
if [ $UPDATE_CROWDIN_FROM_NUXEO = true ]; then
    update_crowdin $PROJECT $NUXEO_MOBILE_PATH/src/i18n/i18n.json
fi

#
# Crowdin -> Nuxeo Mobile update
#
if [ $UPDATE_NUXEO_FROM_CROWDIN = true ]; then
    update_nuxeo $PROJECT $FORMAT $NUXEO_MOBILE_PATH/src/i18n

    cd $NUXEO_MOBILE_PATH
    git diff --quiet || {
        echo "Spotted changes on external translation files"
        git_create_branch
        git_commit "Automatic update of translations from Crowdin"
    }
    git_status
cd $HERE
fi

#
# Push changes to GitHub
#
cd $NUXEO_MOBILE_PATH
git_push
cd $HERE
