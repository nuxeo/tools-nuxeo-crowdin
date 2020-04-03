#!/bin/bash -xe
# Bash script for jenkins, expected to be executed from a workspace
# with the following structure:
# - nuxeo
# - tools-nuxeo-crowdin
#
# Directory "nuxeo" is a checkout of the nuxeo root, without addons
# (which are retrieved by this script).
#
# The addon nuxeo-platform-lang-ext is changed by this script.  Its
# unit tests are run to check validity of aggregated properties to
# send to Crowdin at next automatic syncrhonization.
#
# Parameters:
# - BRANCH: Nuxeo branch to work (master by default)
#

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
LANG_EXT_ROOT=$NUXEO_PATH/modules/platform/nuxeo-platform-lang-ext

#
# Init parameters
#
if [ -z ${BRANCH+x} ]; then
    BRANCH="master"
fi

#
# Nuxeo -> Crowdin update
#
echo Generating aggregated messages.properties file from Nuxeo sources
$SCRIPT_PATH/../nuxeo_aggregates.py $NUXEO_PATH $LANG_EXT_ROOT/src/main/resources/crowdin
echo Aggregate done

cd $LANG_EXT_ROOT
mvn clean verify
cd $HERE
