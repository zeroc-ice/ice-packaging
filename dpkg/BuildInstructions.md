# Building Ubuntu Packages

This document describes how to create source and binary DEB packages for Ice as a regular (non-root) user on your Ubuntu Linux system.

## Setup the packaging software

First we'll install all the tools needed to build the Ice packages on your Ubuntu system:

    $ sudo apt-get install packaging-dev

## Add the ZeroC repository

Some of the third-party packages required to build Ice are not available through Ubuntu repositories, so you need to add the ZeroC Ice repository to be able to install these packages.

First you need to install the GPG key used to sign the packages:

    $ wget https://zeroc.com/download/GPG-KEY-zeroc-release
    $ sudo apt-key add GPG-KEY-zeroc-release

After installing the GPG key, add the ZeroC repository to your system apt sources:

    $ cd /etc/apt/sources.list.d
    $ sudo wget https://zeroc.com/download/Ice/3.6/ubuntu/ice3.6-trusty.list
    $ sudo apt-get update

## Install Ice third-party dependencies

Now we will install the necessary third-party packages from the Ubuntu Software repository.

A Java development kit is required. We recommend that you use Oracle Java 7 to build Ice because the Metrics Graph feature of the IceGrid Administrative console requires JavaFX. If you build Ice using another Java 7 JDK, the Metrics Graph functionality will not be available.

There are several ways to get Oracle Java 7 installed in Ubuntu, but the simplest is to use the ```webupd8team ppa``` repository:

    $ sudo add-apt-repository ppa:webupd8team/java
    $ sudo apt-get update

The next command installs all of the third-party dependencies, including Oracle Java 7 if necessary:

    $ sudo apt-get build-dep zeroc-ice3.6

## Building the Ice packages

Install the Ice 3.6 source distribution:

    $ mkdir ~/zeroc-build
    $ cd ~/zeroc-build
    $ apt-get source zeroc-ice3.6

Change the working directory to ```zeroc-ice3.6-3.6.0```:

    $ cd zeroc-ice3.6-3.6.0

Now you're ready to build the Ice packages:

    $ dpkg-buildpackage -us -uc

The resulting unsigned ```.deb``` files will be in the ```zeroc-build``` directory.

## Applying a patch

Refer to the [Debian documentation](https://www.debian.org/doc/manuals/maint-guide/dother.en.html#patches) for information on incorporating patches into the build.
