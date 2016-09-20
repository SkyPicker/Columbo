#! /bin/sh
# Repository operations

USERID=$1  # Github ID
LOGIN=$2  # Github login
REPOID=$3  # Repository ID
REPONAME=$4  # Repository name
REPOURL=$5  # Github repository url
REPOSTORE="/tmp/repo"  # TODO: Get this from global config later
REPORTSPATH="$REPOSTORE/.reports"

# Tools binaries
bin_git=/usr/bin/git
bin_coala=/usr/bin/coala
bin_cloc=/usr/bin/cloc

# Create path for the user repos
mkdir -p "$REPORTSPATH"
mkdir -p "$REPOSTORE/$LOGIN"

get_config_value() {
    local value=$1
    local config_val=$(awk -v f=$value -F "=" '/f/ {print $2}' config.ini | xargs)
    echo "$config_val"
}

# Clone repository
repopath="$REPOSTORE/$LOGIN/$REPONAME"
echo "$repopath"
if [ -e "$repopath" ];
then
    pull_existing=$(get_config_value "pull_existing")
    echo "$pull_existing"
    if [ "$pull_existing" == "false" ]; then
        echo "config value 'pull_existing = false', exiting.."
        exit
    fi
    cd "$repopath"
    $bin_git pull
else
    $bin_git clone "$REPOURL" "$repopath"
    cd "$repopath"
fi

#########################
# Reports, add more here:
#########################
gen_reportname() {
    local reportid=$1
    local reportname="$REPORTSPATH/${USERID}_${REPOID}_${reportid}"
    echo "$reportname"
}

# Languages, LOC count etc.
reportid="cloc"
reportname=$(gen_reportname "$reportid")
echo "$reportname"
$bin_cloc "$repopath" > "$reportname"
