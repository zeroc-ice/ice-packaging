# Building Linux RPM Packages

This README describes how to create source and binary RPM packages for Ice
as a regular (non-root) user on your Linux system.

## The .rpmmacros File

Create a file named `.rpmmacros` in your home directory similar to the following:

    %_signature gpg
    %_gpg_path /home/rpmbuilder/.gnupg
    %_gpg_name ZeroC, Inc. (release key) <support@zeroc.com>
    %_gpgbin /usr/bin/gpg
    %vendor ZeroC, Inc.
    %dist .el7

The GPG settings are only needed if you want to sign your RPMs. Replace
`/home/rpmbuilder` with a path name that is appropriate for your system.

The value for `%dist` should be one of

    .sles12
    .el7
    .amzn1

These tags correspond to the Linux RPM distributions provided by ZeroC.

Optional macros can be set to customize the RPMs:

* `nameprefix` : defines the prefix to use for RPM package names. For example,
if it's defined to `zeroc-`, the RPM for glacier2 will be named `zeroc-glacier2`
and the RPM for `libice3.7-c++` will be named `libzeroc-ice3.7-c++`.

* `ice_license` : defines the license shown in the RPM information (default
value is `GPLv2 with exceptions`).

* `biarch` : on Red Hat Enterprise Linux 7, set `biarch` to `1` to generate packages for both `x86_64` and `i686`.

## The RPM package build directory

The RPM package build directory is usually `~/rpmbuild`.

## RPM build prerequisites

First install ZeroC's key to avoid warnings with unsigned packages:

    $ wget https://zeroc.com/download/GPG-KEY-zeroc-release
    $ sudo rpm --import GPG-KEY-zeroc-release

Then add the Ice repository for you system and install the source RPM:

* Red Hat Enterprise Linux 7:

    ```
    $ cd /etc/yum.repos.d
    $ sudo wget https://zeroc.com/download/rpm/zeroc-ice-el7.repo
    ```

* Amazon Linux:

    ```
    $ cd /etc/yum.repos.d
    $ sudo wget https://zeroc.com/download/rpm/zeroc-ice-amzn1.repo
    ```

* Suse Linux Enterprise Server 12:

    ```
    $ wget https://zeroc.com/download/rpm/zeroc-ice-sles12.repo
    $ sudo zypper addrepo zeroc-ice-sles12.repo
    ```

Now download and install the source rpm:

    $ yumdownloader --source ice
    $ rpm -i ice-3.7a4-1.el7.src.rpm

You can find the `ice.spec` file in the `~/rpmbuild/SPECS` directory, while the archive
file is in the `~/rpmbuild/SOURCES` directory.

The `ice.spec` file defines a number of build requirements that must be installed on
your system in order to build the RPM packages.

## Creating the source RPM package

Follow these steps to create the Ice source RPM:

1. Copy all desired source files and patches into the directory `~/rpmbuild/SOURCES`

2. Review `ice.spec` to ensure all necessary source files and patches are listed
   using `SourceX` and `PatchX` directives. The files listed here will be included
   in the source RPM.

3. Run rpmbuild:

        $ rpmbuild -bs --sign ice.spec

Omit the `--sign` option if you do not want to sign the source RPM, or if you do
not have a GnuPG key prepared.

The source RPM is created in `~rpmbuild/SRPMS`.

## Creating the binary RPM packages

To create binary RPM packages for Ice, you must first install the source RPM:

    $ rpm -i ice-3.7a4-1.src.rpm

If you have not already done so, install the RPM prerequisites listed in `ice.spec`. 
The following additional steps are also necessary:

- Install the Java Development Kit version 1.8 and verify that the `javac `command
is present in your `PATH`.

- If you want to sign the IceGridGUI jar file, you should set
these environment variables:

   JARSIGNER_KEYSTORE=<path to the keystore file with the certificate>
   JARSIGNER_KEYSTORE_ALIAS=<alias of the certificate>
   JARSIGNER_KEYSTORE_PASSWORD=<keystore file password>

   If you don't set them, the jar file signing will be skipped.

- Build the RPMs as a non-root user.

On Red Hat Enterprise Linux 7 with bi-arch support (x86_64 and i686):

    $ cd ~/rpmbuild/SPECS
    $ rpmbuild -bb --sign --target noarch,i686,x86_64 ice.spec

On Red Hat Enterprise Linux 7 for a single architecture, SuSE Linux Enterprise Server 12 or Amazon Linux:

    $ cd ~/rpmbuild/SPECS
    $ rpmbuild -bb --sign --target noarch,x86_64 ice.spec

Omit the `--sign` option if you do not want to sign the RPMs, or if you do not
have a GnuPG key setup.

Upon completion, the binary RPMs can be found in `~/rpmbuild/RPMS`.

## Applying a Patch

Follow these steps to create a new set of RPMs that incorporates one or more
source patches:

- Install the Ice source RPM
- Edit `ice.spec`:
   - Modify the Release setting, for example:

             # Second build by ACME, Inc.:
             Release: 2acme%{?dist}

    - List the patch (or patches) after ``Source0``, for example:

             Source0: Ice-3.7a4.tar.gz
             Patch1: Ice-3.7a4-patch1.patch
             Patch2: Ice-3.7a4-patch2.patch

    - Apply the patch(es) in the `%prep` section. Continuing our example with
      two patches:

             %prep
             %if %{buildall}
             %setup -n Ice-3.7a4 -q
             %patch1 -p0 -b .orig1
             %patch2 -p0 -b .orig2
             %endif

- Copy the patch(es) to `~/rpmbuild/SOURCES`

- Finally, create the source and binary RPM packages as described above.
