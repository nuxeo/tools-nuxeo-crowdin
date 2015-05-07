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
# - KEY: Crowdin project API key
# - BRANCH: Nuxeo branch to work (master by default)
# - COMMIT_BRANCH: if not blank, branch to work on, created from $BRANCH
# - JIRA: if not blank, jira issue to reference on commit message
#
# Boolean params for corresponding actions:
# - UPDATE_CROWDIN_FROM_NUXEO (default to false if var unset)
# - UPDATE_NUXEO_FROM_CROWDIN (default to false if var unset)
# - DRYRUN: if set to true, changes will not be pushed to Github and
#   Crowdin (default to true if var unset)

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

#
# Init parameters
#
if [ -z ${PROJECT+x} ]; then
    PROJECT="nuxeo"
fi
if [ -z ${BRANCH+x} ]; then
    BRANCH="master"
fi

DO_PUSH=false
if [ -z ${UPDATE_CROWDIN_FROM_NUXEO+x} ]; then
    UPDATE_CROWDIN_FROM_NUXEO=false
fi
if [ -z ${UPDATE_NUXEO_FROM_CROWDIN+x} ]; then
    UPDATE_NUXEO_FROM_CROWDIN=false
fi

if [ -z ${DRYRUN+x} ]; then
    DRYRUN=true
fi
DRYRUN_CMD=""
if [ $DRYRUN = true ]; then
    DRYRUN_CMD="--dry-run"
fi

COMMIT_BRANCH_CREATED=false

# clone all addons
cd $NUXEO_PATH
./clone.py $BRANCH
cd $HERE

#
# Nuxeo -> Crowdin update
#
if [ $UPDATE_CROWDIN_FROM_NUXEO = true ]; then
    echo Updating Crowdin from Nuxeo
    $SCRIPT_PATH/../nuxeo_aggregates.py $NUXEO_PATH $LANG_EXT_ROOT/src/main/resources/crowdin
    echo Aggregate done

    cd $LANG_EXT_ROOT
    git diff --quiet || {
	echo "Spotted changes on reference messages file"
	if [ ! -z $COMMIT_BRANCH ]; then
            # maybe checkout a branch
	    echo "Creating branch $BRANCH"
	    git checkout -b $COMMIT_BRANCH
	    COMMIT_BRANCH_CREATED=true
	fi
	mvn clean verify
	MSG_COMMIT="Automatic merge of reference messages for Crowdin"
	if [ ! -z $JIRA ]; then
	    MSG_COMMIT="$JIRA: $MSG_COMMIT"
	fi
	git commit -m "$MSG_COMMIT" .
	DO_PUSH=true

        # send to Crowdin
	if [ $DRYRUN = false ]; then
	    cd $HERE
	    $SCRIPT_PATH/../crowdin_updater.py $PROJECT $KEY --uc -f $LANG_EXT_ROOT/src/main/resources/crowdin/messages.properties
	fi
    }
    cd $HERE
fi

#
# Crowdin -> Nuxeo update
#
if [ $UPDATE_NUXEO_FROM_CROWDIN = true ]; then
    echo Updating Nuxeo from Crowdin
    $SCRIPT_PATH/../crowdin_updater.py $PROJECT $KEY --un -o $LANG_EXT_ROOT/src/main/resources/web/nuxeo.war/WEB-INF/classes

    cd $LANG_EXT_ROOT
    git diff --quiet || {
	echo "Spotted changes on ext messages files"
	if [ ! -z $COMMIT_BRANCH ]; then
            # maybe checkout a branch
	    if [ $COMMIT_BRANCH_CREATED = false ]; then
		echo "Creating branch $BRANCH"
		git checkout -b $COMMIT_BRANCH
		COMMIT_BRANCH_CREATED=true
	    fi
	fi
	mvn clean verify
	MSG_COMMIT="Automatic update of messages from Crowdin"
	if [ ! -z $JIRA ]; then
	    MSG_COMMIT="$JIRA: $MSG_COMMIT"
	fi
	git commit -m "$MSG_COMMIT" .
	DO_PUSH=true
    }

    if git status --porcelain | grep "^??"; then
	echo "Spotted new languages"
	git status
    fi

    cd $HERE
fi

# actual push of changes
if [ $DO_PUSH = true ]; then
    cd $LANG_EXT_ROOT
    if [ ! -z $COMMIT_BRANCH ]; then
	git push origin $COMMIT_BRANCH $DRYRUN_CMD
    else
	git push origin $BRANCH $DRYRUN_CMD
    fi
    cd $HERE
fi