# Building Linux RPM Packages

This README describes how to create source and binary RPM packages for Ice
as a regular (non-root) user on your Linux system.

## The .rpmmacros File

If building RPMs for Amazon Linux AMI or SLES 12, you need to create a file
named `.rpmmacros` in your home directory with the following content:
```
    %dist .amzn1
```

The value for `%dist` should be one of
```
    .amzn1
    .sles12
```

Defining the `%dist` macro is only necessary for these distributions, for other
supported distributions you don't need to define it.

Optional macros can be set in this file to customize the RPMs:

* `nameprefix` : defines the prefix to use for RPM package names. For example,
if it's defined to `zeroc-`, the RPM for glacier2 will be named `zeroc-glacier2`
and the RPM for `libice3.7-c++` will be named `libzeroc-ice3.7-c++`.

* `ice_license` : defines the license shown in the RPM information (default
value is `GPLv2 with exceptions`).

## The RPM package build directory

The RPM package build directory is usually `~/rpmbuild`.

## RPM build prerequisites

First install ZeroC's key to avoid warnings with unsigned packages:
```
    $ wget https://zeroc.com/download/GPG-KEY-zeroc-release
    $ sudo rpm --import GPG-KEY-zeroc-release
```

Then add the Ice repository for your system and install the source RPM:

* Red Hat Enterprise Linux 7:
```
     $ cd /etc/yum.repos.d
     $ sudo wget https://zeroc.com/download/ice/3.7/el7/zeroc-ice3.7.repo
```

* Amazon Linux AMI:
```
     $ cd /etc/yum.repos.d
     $ sudo wget https://zeroc.com/download/ice/3.7/amzn1/zeroc-ice3.7.repo
```

* Amazon Linux 2:
```
     $ cd /etc/yum.repos.d
     $ sudo wget https://zeroc.com/download/ice/3.7/amzn2/zeroc-ice3.7.repo
```

* SUSE Linux Enterprise Server 12:
```
     $ wget https://zeroc.com/download/ice/3.7/sles12/zeroc-ice3.7.repo
     $ sudo zypper addrepo zeroc-ice3.7.repo
```

Now download and install the source RPM:
```
     $ yumdownloader --source ice
     $ rpm -i ice-3.7.2-1.el7.src.rpm
```

You can find the `ice.spec` file in the `~/rpmbuild/SPECS` directory, while the
archive files are in the `~/rpmbuild/SOURCES` directory.

The `ice.spec` file defines a number of build requirements that must be
installed on your system in order to build the RPM packages.

## Creating the source RPM package

Follow these steps to (re-)create the Ice source RPM:

1. Copy all desired source files and patches into the directory `~/rpmbuild/SOURCES`

2. Review `ice.spec` to ensure all necessary source files and patches are listed
   using `SourceX` and `PatchX` directives. The files listed here will be
   included in the source RPM.

3. Run rpmbuild:
```
      $ rpmbuild -bs ice.spec
```

The source RPM is created in `~rpmbuild/SRPMS`.

## Creating the binary RPM packages

To create binary RPM packages for Ice, you must first install the source RPM:
```
      $ rpm -i ice-3.7.2-1.src.rpm
```
If you have not already done so, install the RPM prerequisites listed in `ice.spec`.
The following additional steps are also necessary:

- Install the Java Development Kit version 1.8 and verify that the `javac`
  command is present in your `PATH`.

- Build the RPMs as a non-root user.
```
      $ cd ~/rpmbuild/SPECS
      $ rpmbuild -bb ice.spec
```

On Red Hat Enterprise Linux 7, your can optionally cross-compile i686 RPMs on a
x86_64 host:
```
      $ setarch i686 rpmbuild -bb ice.spec
```
Upon completion, all the binary RPMs can be found in `~/rpmbuild/RPMS`.
