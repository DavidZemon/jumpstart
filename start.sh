#!/bin/sh

if [ "/do/not/work/here" = "${PWD}" ] ; then
    echo "Welcome to jumpstart! The recommended way to execute jumpstart is by"
    echo "saving these lines to a script named 'jumpstart'."
    echo
    echo "For detailed instructions, please visit"
    echo "  https://github.com/DavidZemon/jumpstart"
    echo
    echo '#!/bin/bash'
    echo 'set -e'
    echo 'set -x'
    echo 'docker pull davidzemon/jumpstart:latest'
    echo 'docker run -it --rm \'
    echo '    -u "$(id -u):$(id -g)" \'
    echo '    -v "$(pwd):$(pwd)" \'
    echo '    -w "$(pwd)" \'
    echo '    davidzemon/jumpstart:latest "$@"'
else
    /usr/local/bin/python3 /opt/jumpstart/jumpstart.py "$@"
fi
