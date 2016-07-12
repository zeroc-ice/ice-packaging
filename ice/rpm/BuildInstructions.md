# Building Linux RPM Packages

This document describes how to create source and binary RPM packages for Ice
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

These tags correspond to the Linux distributions that ZeroC officially supports.

Optional macros can be set to customize the RPMs:

* `nameprefix` : defines the prefix to use for RPM package names. For example,
if it's defined to `zeroc-`, the RPM for glacier2 will be named `zeroc-glacier2`
and the RPM for `libice3.6` will be named `libzeroc-ice3.6`.

* `ice_license` : defines the license shown in the RPM information (default
value is `GPL v2 with exceptions`).

## The RPM package build directory

The RPM package build directory is `/usr/src/packages` on SLES. For RHEL and
Amazon Linux, create and use `~/rpmbuild`. In this document we refer to the
package directory symbolically as `pkgdir`.

You may need to adjust the permissions on all subdirectories of this directory
to be able to create RPM packages as a non-root user.

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
    $ rpm -i ice-3.7a3-1.el7.src.rpm

You can find the `ice.spec` file in the `pkgdir/SPECS` directory, while the archive
file is in the `pkgdir/SOURCES` directory.

The `ice.spec` file defines a number of build requirements that must be installed on
your system in order to build the RPM packages. These dependencies are listed below:

| Package            | Platform                     |
| -------------------| -----------------------------|
| mcpp-devel         | All                          |
| lmdb-devel         | All                          |
| openssl-devel      | All                          |
| javapackages-tools | el7                          |
| jpackage-utils     | amzn1                        |
| bzip2-devel        | All                          |
| expat-devel        | All                          |
| php-devel          | el7, amzn1                   |
| php5-devel         | sles12                       |

The `mcpp-devel` and `lmdb-devel` RPMs are provided by ZeroC. You can determine
the version requirements for all other prerequisites by examining the
`BuildRequires` directives in the `ice.spec` file.

## Creating the source RPM package

Follow these steps to create the Ice source RPM:

1. Copy all desired source files and patches into the directory `pkgdir/SOURCES`

2. Review `ice.spec` to ensure all necessary source files and patches are listed
   using `SourceX` and `PatchX` directives. The files listed here will be included
   in the source RPM.

3. Run rpmbuild:

        $ rpmbuild -bs --sign ice.spec

Omit the `--sign` option if you do not want to sign the source RPM, or if you do
not have a GnuPG key prepared.

The source RPM is created in `pkgdir/SRPMS`.

## Creating the binary RPM packages

To create binary RPM packages for Ice, you must first install the source RPM:

    $ rpm -i ice-3.7a3-1.src.rpm

If you have not already done so, install the RPM prerequisites listed above. The
following additional steps are also necessary:

- Install the Java Development Kit version 1.7 and verify that the javac command
is present in your PATH

   > JDK 1.7 with JavaFX is necessary for compiling the IceGrid Admin GUI client
   > with full functionality. We recommend using Oracle JDK.

- If you want to sign the IceGrid Administrative GUI jar file, you should set
these environment variables:

   JARSIGNER_KEYSTORE=<path to the keystore file with the certificate>
   JARSIGNER_KEYSTORE_ALIAS=<alias of the certificate>
   JARSIGNER_KEYSTORE_PASSWORD=<keystore file password>

   If you don't set them, the jar file signing will be skipped.

- Build the RPMs as a non-root user.

On Red Hat Enterprise Linux 7:

    $ cd pkgdir/SPECS
    $ rpmbuild -bb --sign --target noarch,i686,x86_64 ice.spec

On SuSE Linux Enterprise Server 12 and Amazon Linux:

    $ cd pkgdir/SPECS
    $ rpmbuild -bb --sign --target noarch,x86_64 ice.spec

Omit the `--sign` option if you do not want to sign the RPMs, or if you do not
have a GnuPG key setup.

Upon completion, the binary RPMs can be found in `pkgdir/RPMS`.

## Applying a Patch

Follow these steps to create a new set of RPMs that incorporates one or more
source patches:

- Install the Ice source RPM
- Edit `ice.spec`:
   - Modify the Release setting, for example:

             # Second build by ACME, Inc.:
             Release: 2acme%{?dist}

    - List the patch (or patches) after ``Source0``, for example:

             Source0: Ice-3.7a3.tar.gz
             Patch1: Ice-3.7a3-patch1.patch
             Patch2: Ice-3.7a3-patch2.patch

    - Apply the patch(es) in the `%prep` section. Continuing our example with
      two patches:

             %prep
             %if %{buildall}
             %setup -n Ice-3.7a3 -q
             %patch1 -p0 -b .orig1
             %patch2 -p0 -b .orig2
             %endif

- Copy the patch(es) to `pkgdir/SOURCES`

- Finally, create the source and binary RPM packages as described above.
