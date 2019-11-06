## DMARC-Compliant ListServ Message Constructor

**NOTICE!  The GitHub repository is simply a mirror of the GitLab repository.  All development now takes place on GitLab.
Please do not open issues on GitHub, they will get no attention at all and not be addressed.**

### Basic Information

<table>
<tr><td align=center valign=center><a href="http://www.gnu.org/licenses/agpl-3.0" target="_blank"><img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" title="AGPL 3.0" /></a></td></tr>
<tr><td align=center valign=center><a href="https://pypi.python.org/pypi/dmarcmsg" target="_blank"><img src="http://img.shields.io/pypi/v/dmarcmsg.svg" title="PyPI Version" /></a></td></tr>
<tr><td align=center valign=center><img src="https://img.shields.io/pypi/pyversions/dmarcmsg.svg" title="Python >= 3.5" /></td></tr>
</table>


### Continuous Integration Status

| CI Provider           | Status                                                                                                                                                          |
|:---------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------:|
| GitLab CI             | [![GitLab CI Pipeline](https://gitlab.com/teward/dmarcmsg/badges/master/pipeline.svg)](https://gitlab.com/teward/dmarcmsg/commits/master) |
| Appveyor              | [![Build status](https://ci.appveyor.com/api/projects/status/8ijyg4jg8116nxxf?svg=true)](https://ci.appveyor.com/project/teward/dmarcmsg) |
| TravisCI (via GitHub) | [![Build Status](https://travis-ci.org/teward/dmarcmsg.svg?branch=master)](https://travis-ci.org/teward/dmarcmsg)                         |

## Description

This module and its correpsonding packages are designed to utuilze the existing email message functions but to expand
upon them to create DMARC-compliant messages that a ListServ can send out as itself on behalf of others.

It has the ability to take existing emails and, while retaining the original payloads of the first email, construct a
new email Message instance that can be manipulated like standard email message objects but with ListServ bits added and 
by modifying the From, To, Reply-To, and other relevant headers to allow the email origin points for DMARC compliance 
checks to originate from the ListServ's domain.  This helps to allow valid DKIM and SPF checks.

The only downside is that original validation items from the original message are lost in this current version of the 
package.


## Compatibility
This module was initially created to be both Python 2 and Python 3 comaptible.

However, as of version 0.2.0, the package is only Python 3 compatible.

Please do not use Python 2 with this library.


## Installation / Usage

### Use PyPI

This library is available from the PyPI repository.
    
#### Python 3:
    
    pip3 install dmarcmsg


#### Installing / Importing in Code

Simply copy the `dmarcmsg` package folder into your working directory for your Python script or program.

## Usage

The bulk of this library is designed to generate messages, but is ultimately fairly simple to use.

Command and usage details can be found [here](https://gitlab.com/teward/dmarcmsg/wiki/Commands-and-Usage).

## FAQ

### Where can I report issues or make Feature Requests?

Issues can be reported on the [GitLab repository's Issues section.](https://gitlab.com/teward/dmarcmsg/issues)
