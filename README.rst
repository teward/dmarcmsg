DMARC-Compliant ListServ Message Constructor
--------------------------------------------

Basic Information
~~~~~~~~~~~~~~~~~

.. raw:: html

   <table>

.. raw:: html

   <tr>

.. raw:: html

   <td align="center" valign="center">

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td align="center" valign="center">

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

Continuous Integration Status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+---------------+---------------+
| CI Provider   | Status        |
+===============+===============+
| Travis CI     | |Travis-CI|   |
+---------------+---------------+
| CircleCI      | |CircleCI|    |
+---------------+---------------+

Description
-----------

This module and its correpsonding packages are designed to utuilze the
existing email message functions but to expand upon them to create
DMARC-compliant messages that a ListServ can send out as itself on
behalf of others.

It has the ability to take existing emails and, while retaining the
original payloads of the first email, construct a new email Message
instance that can be manipulated like standard email message objects but
with ListServ bits added and by modifying the From, To, Reply-To, and
other relevant headers to allow the email origin points for DMARC
compliance checks to originate from the ListServ's domain. This helps to
allow valid DKIM and SPF checks.

The only downside is that original validation items from the original
message are lost in this current version of the package.

Compatibility
-------------

This module was written to be both Python 2 and Python 3 compatible, and
as such should work properly without any additional efforts to make it
work on either system.

Installation / Usage
--------------------

Use PyPI
~~~~~~~~

This library is available from the PyPI repository.

Python 2:
^^^^^^^^^

::

    pip install dmarcmsg

Python 3:
^^^^^^^^^

::

    pip3 install dmarcmsg

Installing / Importing in Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simply copy the ``imaplibext`` package folder into your working
directory for your Python script or program.

Usage
-----

The bulk of this library is designed to generate messages, but is
ultimately fairly simple to use.

Command and usage details can be found
`here <https://github.com/teward/dmarcmsg/wiki/Commands-and-Usage>`__.

FAQ
---

Where can I report issues or make Feature Requests?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Issues can be reported on the `GitHub repository's Issues
section. <https://github.com/teward/dmarcmsg/issues>`__

.. |Travis-CI| image:: https://travis-ci.org/teward/imaplibext.svg?branch=master
   :target: https://travis-ci.org/teward/dmarcmsg
.. |CircleCI| image:: https://circleci.com/gh/teward/imaplibext.svg?style=shield
   :target: https://circleci.com/gh/teward/dmarcmsg
