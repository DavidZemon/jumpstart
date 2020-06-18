#!/bin/sh

if [ "yes" = "${JUMPSTART_PRINT_SCRIPT}" ] ; then
    echo "Welcome to jumpstart! The recommended way to execute jumpstart is by"
    echo "saving these lines to a script named 'jumpstart'."
    echo
    echo '#!/bin/bash'
    echo 'set -e'
    echo 'set -x'
    echo 'docker pull davidzemon/jumpstart'
    echo 'docker run -it --rm \'
    echo '    -e JUMPSTART_PRINT_SCRIPT=no \'
    echo '    -u "$(id -u):$(id -g)" \'
    echo '    -v "$(pwd):$(pwd)" \'
    echo '    -w "$(pwd)" \'
    echo '    davidzemon/jumpstart "$@"'
else
    /usr/bin/python3 /opt/jumpstart/jumpstart.py "$@"
fi
