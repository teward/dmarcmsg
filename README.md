## DMARC-Compliant ListServ Message Constructor

### Basic Information

<table>
<tr><td align=center valign=center><a href="http://www.gnu.org/licenses/agpl-3.0" target="_blank"><img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" title="AGPL 3.0" /></a></td></tr>
<tr><td align=center valign=center><a href="https://pypi.python.org/pypi/dmarcmsg" target="_blank"><img src="http://img.shields.io/pypi/v/dmarcmsg.svg" title="PyPI Version" /></a></td></tr>
</table>


### Continuous Integration Status

| CI Provider | Status                                                                                                                                                              |
|:-----------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Travis CI   | [![Travis-CI](https://travis-ci.org/teward/dmarcmsg.svg?branch=master)](https://travis-ci.org/teward/dmarcmsg)                                                  |
| CircleCI    | [![CircleCI](https://circleci.com/gh/teward/dmarcmsg.svg?style=shield)](https://circleci.com/gh/teward/dmarcmsg)                                                |


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
This module was written to be both Python 2 and Python 3 compatible, and as such should work properly without any 
additional efforts to make it work on either system.



## Installation / Usage

### Use PyPI

This library is available from the PyPI repository.

#### Python 2:

    pip install dmarcmsg
    
#### Python 3:
    
    pip3 install dmarcmsg


#### Installing / Importing in Code

Simply copy the `imaplibext` package folder into your working directory for your Python script or program.

## Usage

The bulk of this library is designed to generate messages, but is ultimately fairly simple to use.

Command and usage details can be found [here](https://github.com/teward/dmarcmsg/wiki/Commands-and-Usage).

## FAQ

### Where can I report issues or make Feature Requests?

Issues can be reported on the [GitHub repository's Issues section.](https://github.com/teward/dmarcmsg/issues)
