# coding=utf-8

import datetime
import email
import email.message
import email.utils
from typing import Union


# AnyStr definition in typing has changed since the initial implementation of it for this library,
# such that it is designed to *not* allow mixed types of strings (such as both bytes and str
# objects).  It used to behave instead like Union[str, bytes]. So, we define AnyStr locally here as
# Union[str, bytes] so that code typing systems don't complain about mixed str and bytes for
# AnyStr calls.
AnyStr = Union[str, bytes]


def _construct_dmarc_message(msg: email.message.Message, list_name: AnyStr,
                             list_address: AnyStr, moderated: bool = False,
                             allow_posts: bool = True,
                             quotes_in_from: bool = True) -> email.message.Message:
    """
    Internal function that actually constructs the DMARC compliant message from an email message
    object, which is created/utilized per one of the other three constructor functions.
    :param msg: The email message being converted to DMARC compliant form (required)
    :param list_name: The mailing list name (required)
    :param list_address: The mailing list address (required)
    :param moderated: Whether the list has moderation on it or not (optional, default False)
    :param allow_posts: Whether the list allows posts sent to it (optional, default True)
    :param quotes_in_from: Whether we use single quotes around the components which will construct
    the From field ('noreply@domain.tld' via 'ListServ', for example). (optional, default True)
    :return: email.message.Message object that is DMARC compliant for sending through a DMARC-
    compliant mailing list.
    """

    msg_components = {'To': msg['To'], 'From': msg['From'], 'Subject': msg['Subject']}

    retain_headers = ['to', 'subject', 'from', 'date', 'content-type', 'mime-version',
                      'content-language', 'accept-language', 'auto-submitted', 'precedence',
                      'content-transfer-encoding']

    newmsg = email.message_from_bytes(msg.as_bytes())

    for key in newmsg.keys():
        if str(key).lower() not in retain_headers:
            del newmsg[key]

    # Now, we have to set things properly - note some headers were not retained.

    newmsg['Sender'] = list_address  # New header.

    newmsg.replace_header('To', msg_components['To'])  # Retained, so we replace contents.

    from_ = email.utils.parseaddr(newmsg['From'])

    if quotes_in_from:
        newfromfmt = "'{}' via '{}'"
    else:
        newfromfmt = "{} via {}"
    # From was retained, but has special handling.
    if from_[0] and from_[0] != '':
        # There's a fancy "Real Name" field in here...
        newfrom = email.utils.formataddr((newfromfmt.format(from_[0], list_name), list_address))
    else:
        # ... or there's just a pure email address.
        newfrom = email.utils.formataddr((newfromfmt.format(from_[1], list_name), list_address))

    newmsg.replace_header('From', newfrom)

    newmsg['Reply-To'] = msg_components['From']  # Reply-To is a new header, but was original 'From'

    # And finally, set Message-ID.
    newmsg['Message-ID'] = email.utils.make_msgid()

    # Only add in a new date field if the original date field is missing.
    if 'date' not in [key.lower() for key in newmsg.keys()]:
        # We can pipe the entire datetime into this without going through a time tuple first.
        newmsg['Date'] = email.utils.format_datetime(datetime.datetime.utcnow())

    # Some lists add these next two headers, only add them if present in original message.
    if list_name and list_name != list_address:
        try:
            newmsg.replace_header('List-Id', "{} <{}>".format(list_name, list_address))
        except KeyError:
            newmsg['List-Id'] = "{} <{}>".format(list_name, list_address)
    else:
        try:
            newmsg.replace_header('List-Id', "<{}>".format(list_address))
        except KeyError:
            newmsg['List-Id'] = "<{}>".format(list_address)

    if allow_posts:
        if list_address and list_address != '':
            try:
                newmsg.replace_header('List-Post', "<mailto:{}>".format(list_address))
            except KeyError:
                newmsg['List-Post'] = "<mailto:{}>".format(list_address)

        if moderated:
            newmsg.replace_header('List-Post', newmsg['List-Post'] + " (Postings are Moderated)")
    else:
        try:
            newmsg.replace_header('List-Post', "NO (posting not allowed on this list)")
        except KeyError:
            newmsg['List-Post'] = "NO (posting not allowed on this list)"

    # Precedence: ListServs send mail in 'bulk'.  Other acceptable options are 'list', but
    # we don't do this.
    #
    # Use of the Precedence header is discouraged in RFC 2076 -
    # http://www.faqs.org/rfcs/rfc2076.html
    #
    # try:
    #     newmsg.replace_header('Precedence', 'bulk')
    # except KeyError:
    #     newmsg['Precedence'] = 'bulk'

    return newmsg


def from_string(msg_string: str, list_name: AnyStr, list_address: AnyStr,
                moderated: bool = False, allow_posts: bool = True,
                quotes_in_from: bool = True) -> email.message.Message:
    """
    Constructs a new DMARC compliant listserv email message object from an existing one in a
    string-like object.
    :param msg_string: A string-like object containing the original message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is
    "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is
    "True"
    :param quotes_in_from: Optional, specify if you want to put single quotes around sections of
    the "From" header, such as original sender name and list name. Default is "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent
    out to a list.
    """
    return _construct_dmarc_message(email.message_from_string(msg_string),
                                    list_name, list_address, moderated, allow_posts, quotes_in_from)


def from_bytes(msg_bytes: bytes, list_name: AnyStr, list_address: AnyStr,
               moderated: bool = False, allow_posts: bool = True,
               quotes_in_from: bool = True) -> email.message.Message:
    """
    Constructs a new DMARC compliant listserv email message object from an existing one in a
    bytes-like object.
    :param msg_bytes: A bytes-like object containing the original message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is
    "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is
    "True"
    :param quotes_in_from: Optional, specify if you want to put single quotes around sections of
    the "From" header, such as original sender name and list name. Default is "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent
    out to a list.
    """
    return _construct_dmarc_message(email.message_from_bytes(msg_bytes),
                                    list_name, list_address, moderated, allow_posts, quotes_in_from)


def from_message(msg_obj: email.message.Message, list_name: AnyStr,
                 list_address: AnyStr, moderated: bool = False, allow_posts: bool = True,
                 quotes_in_from: bool = True) -> email.message.Message:
    """
    Constructs a new DMARC compliant listserv email message object from an existing email message
    object.
    :param msg_obj: An instance of email.message.Message containing the original email message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is
    "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is
    "True"
    :param quotes_in_from: Optional, specify if you want to put single quotes around sections of
    the "From" header, such as original sender name and list name. Default is "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent
    out to a list.
    """
    return _construct_dmarc_message(msg_obj, list_name, list_address, moderated, allow_posts,
                                    quotes_in_from)
