# coding=utf-8

import email
import email.utils


def _construct_dmarc_message(msg, list_name, list_address, moderated=False, allow_posts=True):
    msg_components = {'To': msg['To'], 'From': msg['From'], 'Subject': msg['Subject']}

    retain_headers = ['To', 'Subject', 'From', 'Date', 'Content-Type', 'MIME-Version',
                      'Content-Language', 'Accept-Language']

    newmsg = email.message_from_bytes(msg.as_bytes())

    for key in newmsg.keys():
        if key not in retain_headers:
            del newmsg[key]

    # Now, we have to set things properly - note some headers were not retained.

    newmsg['Sender'] = list_address  # New header.

    newmsg.replace_header('To', msg_components['To'])  # Retained, so we replace contents.

    # From was retained, but has special handling.
    if len(newmsg['From'].split('<')) > 1:  # Determine if 'From' is formatted a specific way.
        # If it has 'Thomas Ward <teward@foo.bar>' for example, we need to split out the name for the restructuring.
        newmsg.replace_header('From', "{} via {} <{}>".format(msg_components['From'].split('<')[0].strip(),
                                                              list_name, list_address))
    else:
        # Otherwise, we just use the email address.
        newmsg.replace_header('From', "{} via {} <{}>".format(msg_components['From'].split('<')[0].strip(),
                                                              list_name, list_address))

    newmsg['Reply-To'] = msg_components['From']  # Reply-To is a new header, but was original 'From'

    # But we need to add the ListServ and ourself to the "Cc" list because reasons.
    newmsg['CC'] = '{}; {}'.format(list_address, msg_components['From'])  # New header.

    # And finally, set Message-ID and Date.
    newmsg['Message-ID'] = email.utils.make_msgid()
    newmsg['Date'] = email.utils.formatdate()

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

    return newmsg


def from_string(msg_string, list_name, list_address, moderated=False, allow_posts=True):
    """
    Constructs a new DMARC compliant listserv email message object from an existing one in a string-like object.
    :param msg_string: A string-like object containing the original message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent out to a list.
    """
    return _construct_dmarc_message(email.message_from_string(msg_string),
                                    list_name, list_address, moderated, allow_posts)


def from_bytes(msg_bytes, list_name, list_address, moderated=False, allow_posts=True):
    """
    Constructs a new DMARC compliant listserv email message object from an existing one in a bytes-like object.
    :param msg_bytes: A bytes-like object containing the original message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent out to a list.
    """
    return _construct_dmarc_message(email.message_from_bytes(msg_bytes),
                                    list_name, list_address, moderated, allow_posts)


def from_message(msg_obj, list_name, list_address, moderated=False, allow_posts=True):
    """
    Constructs a new DMARC compliant listserv email message object from an existing email message object.
    :param msg_obj: An instance of email.message.Message containing the original email message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent out to a list.
    """
    return _construct_dmarc_message(msg_obj, list_name, list_address, moderated, allow_posts)
