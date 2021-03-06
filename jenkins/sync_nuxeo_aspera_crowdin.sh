#!/bin/bash -xe
# Bash script for jenkins, expected to be executed from a workspace
# with the following structure:
# - nuxeo-aspera-connector
# - tools-nuxeo-crowdin
#
# Directory "nuxeo-aspera-connector" is a checkout of the nuxeo-aspera-connector repository.
#
# The nuxeo-aspera-connector/nuxeo-aspera-web/src/main/resources/web/nuxeo.war/ui/i18n directory is changed by this script.
#
# Parameters:
# - PROJECT: Crowdin project name (nuxeo-aspera by default)
# - PROJECT_PATH: The local project path (./nuxeo-aspera-connector by default)
# - INPUT_FILE: The input reference file (./nuxeo-aspera-connector/nuxeo-aspera-web/src/main/resources/web/nuxeo.war/ui/i18n/messages.json)
# - OUTPUT_FOLDER: The output folder to which translations will be downloaded (./nuxeo-aspera-connector/nuxeo-aspera-web/src/main/resources/web/nuxeo.war/ui/i18n by default)
# - FORMAT: Crowdin project format (json by default)
# - KEY: Crowdin project API key
# - BRANCH: Nuxeo Web UI branch to work (master by default, see commons.sh)
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

# Include common variables and functions
source $SCRIPT_PATH/common.sh

#
# Init parameters
#
if [ -z ${PROJECT+x} ]; then
    PROJECT="nuxeo-aspera"
fi
if [ -z ${PROJECT_PATH+x} ]; then
    PROJECT_PATH=./nuxeo-aspera-connector
fi
if [ -z ${INPUT_FILE+x} ]; then
    INPUT_FILE=$PROJECT_PATH/nuxeo-aspera-web/src/main/resources/web/nuxeo.war/ui/i18n/messages.json
fi
if [ -z ${OUTPUT_FOLDER+x} ]; then
    OUTPUT_FOLDER=$PROJECT_PATH/nuxeo-aspera-web/src/main/resources/web/nuxeo.war/ui/i18n
fi
if [ -z ${FORMAT+x} ]; then
    FORMAT="json"
fi
if [ -z ${CROWDIN_PARENT_FOLDER+x} ]; then
    CROWDIN_PARENT_FOLDER=""
fi
if [ -z ${UPDATE_CROWDIN_FROM_NUXEO+x} ]; then
    UPDATE_CROWDIN_FROM_NUXEO=false
fi
if [ -z ${UPDATE_NUXEO_FROM_CROWDIN+x} ]; then
    UPDATE_NUXEO_FROM_CROWDIN=false
fi

#
# Nuxeo Aspera Cconnector -> Crowdin update
#
if [ $UPDATE_CROWDIN_FROM_NUXEO = true ]; then
    update_crowdin $PROJECT $INPUT_FILE $CROWDIN_PARENT_FOLDER
fi

#
# Crowdin -> Nuxeo Aspera Cconnector
#
if [ $UPDATE_NUXEO_FROM_CROWDIN = true ]; then
    update_nuxeo $PROJECT $FORMAT $OUTPUT_FOLDER $CROWDIN_PARENT_FOLDER

    cd $PROJECT_PATH
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
cd $PROJECT_PATH
git_push
cd $HERE
