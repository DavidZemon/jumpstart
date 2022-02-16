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

   For detailed instructions, please visit
     https://github.com/DavidZemon/jumpstart

   #!/bin/bash
   set -e
   set -x
   docker pull davidzemon/jumpstart:latest
   docker run -it --rm \
       -u "$(id -u):$(id -g)" \
       -v "$(pwd):$(pwd)" \
       -w "$(pwd)" \
       davidzemon/jumpstart:latest "$@"
   ```
   As the instructions explain, create a script on your `$PATH` with this
   content. Be sure to make the script executable with
   `chmod +x ~/bin/jumpstart`, substituting `~/bin/jumpstart` with whatever
   path you chose for the script.
3. Create an empty directory for your new project and run the newly created
   `jumpstart` script
   ```sh
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

### Provide your own license text

Though the working directory is expected to be empty, there is an exception
built into jumpstart which allows a file with license text to exist in the
working directory. Use this as an easy way to provide your own license text via
the `--license` argument.
