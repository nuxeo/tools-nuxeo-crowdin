#!/bin/bash -xe
# Common variables and functions for the Jenkins scripts.

#
# Variables
#
SCRIPT_PATH="`dirname \"$0\"`"
DO_PUSH=false
COMMIT_BRANCH_CREATED=false

if [ -z ${BRANCH+x} ]; then
    BRANCH="master"
fi
if [ -z ${DRYRUN+x} ]; then
    DRYRUN=true
fi
DRYRUN_CMD=""
if [ $DRYRUN = true ]; then
    DRYRUN_CMD="--dry-run"
fi

#
# Functions
#

# Parameters:
# - $1: Crowdin project name
# - $2: Reference file to upload
# - $3: Parent folder inside Crowdin project (optional)
function update_crowdin() {
    echo Updating Crowdin from Nuxeo
    if [ $DRYRUN = false ]; then
        # upload to Crowdin
        if [ ! -z $3 ]; then
          $SCRIPT_PATH/../crowdin_updater.py $1 --uc -f $2 -p $3
        else
          $SCRIPT_PATH/../crowdin_updater.py $1 --uc -f $2
        fi
    fi
}

# Parameters:
# - $1: Crowdin project name
# - $2: Output directory for translation files
# - $3: Parent folder inside Crowdin project (optional)
function update_nuxeo() {
    echo Updating Nuxeo from Crowdin
    # download from Crowdin
    if [ ! -z $4 ]; then
      $SCRIPT_PATH/../crowdin_updater.py $1 --un -o $2 -p $3
    else
      $SCRIPT_PATH/../crowdin_updater.py $1 --un -o $2
    fi
}

function git_create_branch() {
    if [ ! -z $COMMIT_BRANCH ]; then
        # maybe checkout a branch
        if [ $COMMIT_BRANCH_CREATED = false ]; then
            echo "Creating branch $COMMIT_BRANCH"
            git checkout -b $COMMIT_BRANCH
            COMMIT_BRANCH_CREATED=true
        fi
    fi
}

# Parameters:
# - $1: git commit message
function git_commit() {
    MSG_COMMIT="$1"
    if [ ! -z $JIRA ]; then
        MSG_COMMIT="$JIRA: $MSG_COMMIT"
    fi
    git commit -m "$MSG_COMMIT" .
    DO_PUSH=true
}

function git_status() {
    if git status --porcelain | grep "^??"; then
        echo "Spotted new languages"
        git status
    fi
}

function git_push() {
    if [ $DO_PUSH = true ]; then
        if [ ! -z $COMMIT_BRANCH ]; then
            git push origin $COMMIT_BRANCH $DRYRUN_CMD
        else
            git push origin $BRANCH $DRYRUN_CMD
        fi
    fi
}
