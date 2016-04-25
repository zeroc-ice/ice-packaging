# Building Ubuntu Packages

This document describes how to create source and binary DEB packages for Ice as
a regular (non-root) user on your Ubuntu Linux system.

## Setup the packaging software

First we'll install all the tools needed to build the Ice packages on your Ubuntu
system:

    $ sudo apt-get install packaging-dev

## Install Ice third-party dependencies

Now we will install the necessary third-party packages from the Ubuntu Software
repository.

A Java development kit is required. We recommend that you use Oracle Java 7 to
build Ice because the Metrics Graph feature of the IceGrid Administrative console
requires JavaFX. If you build Ice using another Java 7 JDK, the Metrics Graph
functionality will not be available.

There are several ways to get Oracle Java 7 installed in Ubuntu, but the simplest
is to use the `webupd8team ppa` repository:

    $ sudo add-apt-repository ppa:webupd8team/java
    $ sudo apt-get update

The next command installs all of the third-party dependencies, including Oracle
Java 7 if necessary:

    $ sudo apt-get build-dep zeroc-ice3.7
    
For Ubuntu 16.04 you need to use the nophp5 build profile to avoid php5 dependencies:

    $ sudo DEB_BUILD_PROFILES=nophp5 apt-get build-dep zeroc-ice3.7

## Add the ZeroC source repository

The Ice 3.7 source distribution is available in the ZeroC source repository, you need
to install the source repository correspoding to your distribution:

    $ sudo apt-add-repository "deb-src https://zeroc.com/download/apt/ice/ubuntu`lsb_release -rs` stable main"

## Building the Ice packages

Install the Ice 3.7 source distribution:

    $ mkdir ~/zeroc-build
    $ cd ~/zeroc-build
    $ apt-get source zeroc-ice3.7

Change the working directory to `zeroc-ice3.7-3.7.0`:

    $ cd zeroc-ice3.7-3.7.0

Now you're ready to build the Ice packages:

    $ dpkg-buildpackage -us -uc

Use the nophp5 build profile to disable the building of PHP packages. This is required
with Ubuntu 16.04, which doesn't support php5:

    $ dpkg-buildpackage -us -uc -Pnophp5

The resulting unsigned `.deb` files will be in the `zeroc-build` directory.

## Applying a patch

Refer to the [Debian documentation][1] for information on incorporating patches
into the build.

[1]: https://www.debian.org/doc/manuals/maint-guide/dother.en.html#patches
