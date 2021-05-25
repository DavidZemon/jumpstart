C/C++ Project Jump Start
========================

Generate a C/C++ project using a modern development environment

Instructions
------------

1. Run the jumpstart image once to pull the latest image and print the initial
   help text:
   ```sh
   docker run --rm davidzemon/jumpstart
   ```
2. The following help text will be printed:
   ```txt
   Welcome to jumpstart! The recommended way to execute jumpstart is by
   saving these lines to a script named 'jumpstart'.

   #!/bin/bash
   set -e
   set -x
   docker pull davidzemon/jumpstart
   docker run -it --rm \
       -e JUMPSTART_PRINT_SCRIPT=no \
       -u "$(id -u):$(id -g)" \
       -v "$(pwd):$(pwd)" \
       -w "$(pwd)" \
       davidzemon/jumpstart "$@"
   ```
   As the instructions explain, create a script on your `$PATH` with this
   content. Be sure to make the script executable with
   `chmod +x ~/bin/jumpstart`, substituting `~/bin/jumpstart` with whatever
   path you chose for the script.
3. Create an empty directory for your new project and run the newly created
   `jumpstart` script
   ```
   mkdir ~/sample
   cd ~/sample
   jumpstart
   ```
4. Answer each interactive prompt to configure your new project. Each prompt
   has a default value in square brackets which will be used if no input is
   provided.

Tips
----

### Command-line arguments

Jumpstart exposes each option as a command-line argument, allowing
non-interactive use of the generator. View the available arguments by invoking
the Docker wrapper script with the `-h`/`--help` argument:

```
jumpstart -h
```

### Accept all defaults

To make non-interactive use even easier, a special `--defaults` command-line
argument is exposed. Use this (probably with one or two other command-line
arguments) to quickly generate a project with only minor changes from the
default template. This can be useful for any number of reasons, including
comparing exactly what changes when a specific option is modified.
