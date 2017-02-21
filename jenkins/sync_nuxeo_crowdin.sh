#!/bin/bash -xe
# Bash script for jenkins, expected to be executed from a workspace
# with the following structure:
# - nuxeo
# - tools-nuxeo-crowdin
#
# Directory "nuxeo" is a checkout of the nuxeo root, without addons
# (which are retrieved by this script).
#
# The addon nuxeo-platform-lang-ext is changed by this script.
#
# Parameters:
# - PROJECT: Crowdin project name (nuxeo by default)
# - FORMAT: Crowdin project format (java by default)
# - KEY: Crowdin project API key
# - BRANCH: Nuxeo branch to work (master by default, see commons.sh)
# - COMMIT_BRANCH: if not blank, branch to work on, created from $BRANCH
# - JIRA: if not blank, jira issue to reference on commit message
#
# Boolean params for corresponding actions:
# - UPDATE_CROWDIN_FROM_NUXEO (default to false if var unset)
# - UPDATE_NUXEO_FROM_CROWDIN (default to false if var unset)
# - DRYRUN: if set to true, changes will not be pushed to GitHub and
#   Crowdin (default to true if var unset, see commons.sh)

set -e

echo JAVA_OPTS: $JAVA_OPTS

if [ ! -z $JDK_PATH ]; then
  export JAVA_HOME=$JDK_PATH
  export PATH=$JDK_PATH/bin:$PATH
fi

export PATH=$MAVEN_PATH/bin:$PATH
if [ ! -z $MAVEN_XMX_RELEASE ]
then
    export MAVEN_OPTS="-Xmx$MAVEN_XMX_RELEASE -Xms1g -XX:MaxPermSize=512m"
else
    export MAVEN_OPTS="-Xmx1g -Xms1g -XX:MaxPermSize=512m"
fi

HERE=`pwd`
SCRIPT_PATH="`dirname \"$0\"`"
NUXEO_PATH=./nuxeo
LANG_EXT_ROOT=$NUXEO_PATH/addons/nuxeo-platform-lang-ext

# Include common variables and functions
source $SCRIPT_PATH/common.sh

#
# Init parameters
#
if [ -z ${PROJECT+x} ]; then
    PROJECT="nuxeo"
fi
if [ -z ${FORMAT+x} ]; then
    FORMAT="java"
fi
if [ -z ${UPDATE_CROWDIN_FROM_NUXEO+x} ]; then
    UPDATE_CROWDIN_FROM_NUXEO=false
fi
if [ -z ${UPDATE_NUXEO_FROM_CROWDIN+x} ]; then
    UPDATE_NUXEO_FROM_CROWDIN=false
fi

# clone all addons
cd $NUXEO_PATH
./clone.py $BRANCH
cd addons
# NXBT-1381: extra clone disconnected addons for 8.10
git clone git@github.com:nuxeo/nuxeo-groups-rights-audit.git
git clone git@github.com:nuxeo/nuxeo-travel-expenses.git
cd $HERE

#
# Nuxeo -> Crowdin update
#
if [ $UPDATE_CROWDIN_FROM_NUXEO = true ]; then
    $SCRIPT_PATH/../nuxeo_aggregates.py $NUXEO_PATH $LANG_EXT_ROOT/src/main/resources/crowdin
    echo Aggregate done

    cd $LANG_EXT_ROOT
    git diff --quiet || {
        echo "Spotted changes on reference messages file"
        git_create_branch
        mvn clean verify
        git_commit "Automatic merge of reference messages for Crowdin"
        # send to Crowdin
        cd $HERE
        update_crowdin $PROJECT $LANG_EXT_ROOT/src/main/resources/crowdin/messages.properties
    }
    cd $HERE
fi

#
# Crowdin -> Nuxeo update
#
if [ $UPDATE_NUXEO_FROM_CROWDIN = true ]; then
    update_nuxeo $PROJECT $FORMAT $LANG_EXT_ROOT/src/main/resources/web/nuxeo.war/WEB-INF/classes

    cd $LANG_EXT_ROOT
    git diff --quiet || {
        echo "Spotted changes on ext messages files"
        git_create_branch
        mvn clean verify
        git_commit "Automatic update of messages from Crowdin"
    }
    git_status
    cd $HERE
fi

# actual push of changes
cd $LANG_EXT_ROOT
git_push
cd $HERE
