Red Lion C/C++ Project Jump Start
=================================

Generate a C/C++ project using the Red Lion project style

Instructions
------------

1. Acquire the Docker wrapper script by cloning the project
   ```
   git clone https://github.com/wsbu/jumpstart.git
   
   ```
2. Create a symlink in your `bin` directory to the Docker wrapper script
   ```
   ln -s ~/jumpstart/docker-jumpstart ~/bin/docker-jumpstart
   ```
3. Create an empty directory for your new project and run the Docker wrapper 
   script
   ```
   mkdir ~/sample
   cd ~/sample
   docker-jumpstart
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
docker-jumpstart -h
```

### Accept all defaults

To make non-interactive use even easier, a special `--defaults` command-line 
argument is exposed. Use this (probably with one or two other command-line 
arguments) to quickly generate a project with only minor changes from the
default template. This can be useful for any number of reasons, including
comparing exactly what changes when a specific option is modified.
