The icehashpassword package provides the icehashpassword script which can be used to create passwords compatible with  the Glacier2 crypt permissions verifier.

Installation
============

We recommend using ``pip`` or ``easy_install`` to install this
package.

Home Page
=========

Visit `ZeroC's home page <https://zeroc.com>`_ for the latest news
and information about Ice.

Package Contents
================

The package provides the icehashpassword utility.

Usage:
::

    Usage: icehashpassword [options]

    OPTIONS

      -d MESSAGE_DIGEST_ALGORITHM, --digest=MESSAGE_DIGEST_ALGORITHM
          The message digest algorithm to use with PBKDF2, valid values are (sha1, sha256, sha512).

      -s SALT_SIZE, --salt=SALT_SIZE
          Optional number of bytes to use when generating new salts.

      -r ROUNDS, --rounds=ROUNDS
          Optional number of rounds to use.

      -h, --help
          Show this message.

Support
=======

Join us on our `user forums <https://zeroc.com/forums/forum.php>`_ if you have questions
about this package.
